
import sys
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
from lxml import etree
from shapely.geometry import Polygon, mapping, LinearRing
from shapely.ops import linemerge

OSM_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("C:/Users/vazqu\Downloads\puerto-rico-251109.osm_01.osm")
OUT_GEOJSON = Path("buildings_streamPR.geojson")

def parse_osm_stream(osm_path: Path):

    nodes: Dict[str, Tuple[float, float]] = {}
    building_ways: Dict[str, List[str]] = {}
    ways_tags: Dict[str, Dict[str, str]] = {}
    relations: List[Dict] = []

    context = etree.iterparse(str(osm_path), events=("end",), recover=True)
    for event, elem in context:
        if elem.tag == "node":
            nid = elem.get("id")
            lat = elem.get("lat")
            lon = elem.get("lon")
            if nid and lat and lon:
                nodes[nid] = (float(lon), float(lat))
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        elif elem.tag == "way":
            wid = elem.get("id")
            tags = {}
            nds = []
            for child in elem:
                if child.tag == "tag":
                    k = child.get("k"); v = child.get("v")
                    if k:
                        tags[k] = v
                elif child.tag == "nd":
                    ref = child.get("ref")
                    if ref:
                        nds.append(ref)
            if "building" in tags and tags.get("building", "").lower() not in ("", "no", "false"):
                building_ways[wid] = nds
                ways_tags[wid] = tags
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        elif elem.tag == "relation":
            rel_tags = {}
            members = []
            is_multipolygon = False
            for child in elem:
                if child.tag == "tag":
                    k = child.get("k"); v = child.get("v")
                    if k:
                        rel_tags[k] = v
                        if k == "type" and v == "multipolygon":
                            is_multipolygon = True
                elif child.tag == "member":
                    mtype = child.get("type")
                    ref = child.get("ref")
                    role = child.get("role") or ""
                    members.append({"type": mtype, "ref": ref, "role": role})
            have_building = any(k.startswith("building") for k in rel_tags.keys())
            if is_multipolygon and have_building:
                relations.append({"tags": rel_tags, "members": members, "id": elem.get("id")})
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]


    del context
    return nodes, building_ways, ways_tags, relations

def way_nodes_to_polygon(nd_refs: List[str], nodes: Dict[str, Tuple[float, float]]):
    coords = []
    for ref in nd_refs:
        if ref in nodes:
            coords.append(nodes[ref])
        else:
            return None
    if len(coords) < 4:
        return None
    if coords[0] != coords[-1]:
        coords.append(coords[0])
    try:
        lr = LinearRing(coords)
        if not lr.is_ccw and lr.is_ring:
            poly = Polygon(lr)
        else:
            poly = Polygon(lr)
        if poly.is_valid and poly.area > 0:
            return poly
    except Exception:
        return None
    return None

def assemble_relation_polygon(rel, building_ways, nodes):
    outers = []
    inners = []
    for m in rel["members"]:
        if m["type"] == "way" and m["ref"] in building_ways:
            ref_nds = building_ways[m["ref"]]
            if m["role"] == "inner":
                inners.append(ref_nds)
            else:
                outers.append(ref_nds)

    outer_polys = []
    for nds in outers:
        p = way_nodes_to_polygon(nds, nodes)
        if p:
            outer_polys.append(p)
    if not outer_polys:
        return None

    holes = []
    for nds in inners:
        p = way_nodes_to_polygon(nds, nodes)
        if p:
            holes.append(p.exterior.coords)

    try:
        if len(outer_polys) == 1:
            outer = outer_polys[0]
            hole_coords = [list(h) for h in holes if Polygon(h).within(outer)]
            return Polygon(outer.exterior.coords, holes=hole_coords)
        else:
            merged = linemerge([p.exterior for p in outer_polys])
            polys = [p for p in outer_polys if p.is_valid]
            if polys:
                big = max(polys, key=lambda x: x.area)
                hole_coords = [list(h) for h in holes if Polygon(h).within(big)]
                return Polygon(big.exterior.coords, holes=hole_coords)
    except Exception:
        return None
    return None

def main():
    print("Parsing (stream) OSM:", OSM_PATH)
    nodes, building_ways, ways_tags, relations = parse_osm_stream(OSM_PATH)
    print(f"Nodes stored: {len(nodes)}")
    print(f"Building ways found: {len(building_ways)}")
    print(f"Multipolygon relations found: {len(relations)}")

    features = []

    for wid, nds in building_ways.items():
        poly = way_nodes_to_polygon(nds, nodes)
        if poly:
            props = ways_tags.get(wid, {}).copy()
            props["osm_type"] = "way"
            props["osm_id"] = wid
            features.append({"type": "Feature", "geometry": mapping(poly), "properties": props})

    for rel in relations:
        poly = assemble_relation_polygon(rel, building_ways, nodes)
        if poly:
            props = rel["tags"].copy()
            props["osm_type"] = "relation"
            props["osm_id"] = rel.get("id")
            features.append({"type": "Feature", "geometry": mapping(poly), "properties": props})

    fc = {"type": "FeatureCollection", "features": features}
    OUT_GEOJSON.write_text(json.dumps(fc))
    print(f"Wrote {len(features)} building features to {OUT_GEOJSON}")

if __name__ == "__main__":
    main()


