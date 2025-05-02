"""JSON registry data."""

try:
    import registry_class
except ModuleNotFoundError:
    try:
        from src.jsonid import registry_class
    except ModuleNotFoundError:
        from jsonid import registry_class


_registry = [
    registry_class.RegistryEntry(
        identifier="jrid:0001",
        name=[{"@en": "package lock file"}],
        description=[{"@en": "node manifest file manifestation"}],
        markers=[
            {"KEY": "name", "EXISTS": None},
            {"KEY": "lockfileVersion", "EXISTS": None},
            {"KEY": "packages", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0002",
        name=[{"@en": "ocfl inventory (all versions)"}],
        description=[{"@en": "ocfl inventory file"}],
        markers=[
            {"KEY": "type", "STARTSWITH": "https://ocfl.io/"},
            {"KEY": "type", "CONTAINS": "spec/#inventory"},
            {"KEY": "head", "EXISTS": None},
            {"KEY": "manifest", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0003",
        name=[{"@en": "gocfl config file"}],
        description=[{"@en": "gocfl config file"}],
        markers=[
            {"KEY": "extensionName", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0004",
        name=[{"@en": "dataverse dataset file"}],
        markers=[
            {"KEY": "datasetVersion", "EXISTS": None},
            {"KEY": "publicationDate", "EXISTS": None},
            {"KEY": "publisher", "EXISTS": None},
            {"KEY": "identifier", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0005",
        name=[{"@en": "rocrate (all versions)"}],
        markers=[
            {"KEY": "@context", "STARTSWITH": "https://w3id.org/ro/crate/"},
            {"KEY": "@context", "ENDSWITH": "/context"},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0006",
        name=[{"@en": "ro-crate (1.1)"}],
        markers=[
            {
                "KEY": "@context",
                "IS": [
                    "https://w3id.org/ro/crate/1.1/context",
                    {"@vocab": "http://schema.org/"},
                ],
            },
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0007",
        name=[{"@en": "json schema document"}],
        markers=[
            {"KEY": "$schema", "STARTSWITH": "https://json-schema.org/"},
            {"KEY": "$schema", "ENDSSWITH": "/schema"},
            {"KEY": "$defs", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0008",
        name=[{"@en": "iiif image api (all versions)"}],
        markers=[
            {"KEY": "@context", "STARTSWITH": "http://iiif.io/api/image/"},
            {"KEY": "@context", "ENDSSWITH": "/context.json"},
            {"KEY": "type", "CONTAINS": "ImageService"},
            {"KEY": "protocol", "IS": "http://iiif.io/api/image"},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0009",
        name=[{"@en": "JSON-LD (generic)"}],
        archive_team="http://fileformats.archiveteam.org/wiki/JSON-LD",
        markers=[
            {"KEY": "@context", "EXISTS": None},
            {"KEY": "id", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0010",
        name=[{"@en": "gocfl metafile metadata"}],
        markers=[
            {"KEY": "signature", "EXISTS": None},
            {"KEY": "organisation_id", "EXISTS": None},
            {"KEY": "organisation", "EXISTS": None},
            {"KEY": "title", "EXISTS": None},
            {"KEY": "user", "EXISTS": None},
            {"KEY": "address", "EXISTS": None},
            {"KEY": "created", "EXISTS": None},
            {"KEY": "last_changed", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0011",
        name=[{"@en": "siegfried report (all versions)"}],
        markers=[
            {"KEY": "siegfried", "EXISTS": None},
            {"KEY": "scandate", "EXISTS": None},
            {"KEY": "signature", "EXISTS": None},
            {"KEY": "identifiers", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0012",
        name=[{"@en": "sops encrypted secrets file"}],
        archive_team="http://fileformats.archiveteam.org/wiki/SOPS",
        markers=[
            {"KEY": "sops", "EXISTS": None},
            {"GOTO": "sops", "KEY": "kms", "EXISTS": None},
            {"GOTO": "sops", "KEY": "pgp", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0013",
        name=[{"@en": "sparql query (generic)"}],
        markers=[
            {"KEY": "head", "EXISTS": None},
            {"KEY": "results", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0014",
        name=[{"@en": "wikidata results (generic)"}],
        markers=[
            {"KEY": "head", "EXISTS": None},
            {"KEY": "results", "EXISTS": None},
            {"KEY": "endpoint", "IS": "https://query.wikidata.org/sparql"},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0015",
        name=[{"@en": "google link file"}],
        pronom="http://www.nationalarchives.gov.uk/PRONOM/fmt/1073",
        wikidata="http://www.wikidata.org/entity/Q105856848",
        markers=[
            {"KEY": "url", "STARTSWITH": "https://docs.google.com/open"},
        ],
    ),
    # Also: id can be "bookmarks.json", "inbox.json", "likes.json"
    registry_class.RegistryEntry(
        identifier="jrid:0016",
        name=[{"@en": "activity streams json (generic)"}],
        wikidata="https://www.wikidata.org/entity/Q4677626",
        markers=[
            {"KEY": "@context", "STARTSWITH": "https://www.w3.org/ns/activitystreams"},
            {"KEY": "id", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0017",
        name=[{"@en": "open resume"}],
        description=[{"@en": "an open source data-oriented resume builder"}],
        markers=[
            {"KEY": "basics", "EXISTS": None},
            {"KEY": "work", "EXISTS": None},
            {"KEY": "education", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0018",
        name=[{"@en": "jacker song"}],
        archive_team="http://fileformats.archiveteam.org/wiki/Jacker_song",
        description=[{"@en": "via"}],
        markers=[
            {"KEY": "$schema", "STARTSWITH": "http://json-schema.org/"},
            {"KEY": "$schema", "ENDSWIWITH": "/schema#"},
            {"KEY": "name", "IS": "Document"},
            {"KEY": "is", "IS": "http://largemind.com/schema/jacker-song-1#"},
            {"KEY": "namespace", "IS": "jacker"},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0019",
        name=[{"@en": "JSON Patch"}],
        mime="application/json-patch+json",
        rfc="https://datatracker.ietf.org/doc/html/rfc6902",
        archive_team="http://fileformats.archiveteam.org/wiki/JSON_Patch",
        markers=[
            {"INDEX": 0, "KEY": "op", "EXISTS": None},
            {"INDEX": 0, "KEY": "path", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0020",
        name=[
            {"@en": "GL Transmission Format: GLTF runtime 3D asset library (Generic)"}
        ],
        archive_team="http://fileformats.archiveteam.org/wiki/GlTF",
        markers=[
            {"KEY": "$schema", "STARTSWITH": "http://json-schema.org/"},
            {"KEY": "$schema", "ENDSWIWITH": "/schema#"},
            {"KEY": "title", "EXISTS": None},
            {"KEY": "type", "IS": "object"},
            {"KEY": "description", "IS": "The root object for a glTF asset."},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0021",
        name=[{"@en": "Tweet Object"}],
        pronom="http://www.nationalarchives.gov.uk/PRONOM/fmt/1311",
        wikidata="https://www.wikidata.org/entity/Q85415600",
        markers=[
            {"KEY": "created_at", "ISTYPE": str},
            {"KEY": "id", "ISTYPE": int},
            {"KEY": "id_str", "ISTYPE": str},
            {"KEY": "user", "ISTYPE": dict},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0022",
        name=[{"@en": "sandboxels save file"}],
        pronom="http://www.nationalarchives.gov.uk/PRONOM/fmt/1956",
        markers=[
            {"GOTO": "meta", "KEY": "saveVersion", "EXISTS": None},
            {"GOTO": "meta", "KEY": "gameVersion", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0023",
        name=[{"@en": "dublin core metadata (archivematica)"}],
        markers=[
            {"INDEX": 0, "KEY": "dc.title", "EXISTS": None},
            {"INDEX": 0, "KEY": "dc.type", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0024",
        name=[{"@en": "tika recursive metadata"}],
        markers=[
            {"INDEX": 0, "KEY": "Content-Length", "EXISTS": None},
            {"INDEX": 0, "KEY": "Content-Type", "EXISTS": None},
            {"INDEX": 0, "KEY": "X-TIKA:Parsed-By", "EXISTS": None},
            {"INDEX": 0, "KEY": "X-TIKA:parse_time_millis", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0025",
        name=[{"@en": "JavaScript package.json file"}],
        markers=[
            {"KEY": "name", "EXISTS": None},
            {"KEY": "version", "EXISTS": None},
            {"KEY": "scripts", "EXISTS": None},
            {"KEY": "devDependencies", "EXISTS": None},
            {"KEY": "dependencies", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0026",
        name=[{"@en": "Parcore schema documents"}],
        pronom="http://www.nationalarchives.gov.uk/PRONOM/fmt/1311",
        markers=[
            {"KEY": "$id", "STARTSWITH": "http://www.parcore.org/schema/"},
            {"KEY": "$schema", "EXISTS": None},
            {"KEY": "definitions", "ISTYPE": dict},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0027",
        name=[{"@en": "coriolis.io ship loadout"}],
        wikidata="http://www.wikidata.org/entity/Q105849952",
        markers=[
            {"KEY": "$schema", "CONTAINS": "coriolis.io/schemas/ship-loadout"},
            {"KEY": "name", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0028",
        name=[{"@en": "coriolis.io ship loadout (schema)"}],
        markers=[
            {"KEY": "$schema", "STARTSWITH": "http://json-schema.org/"},
            {"KEY": "$schema", "ENDSWITH": "/schema#"},
            {"KEY": "id", "STARTSWITH": "https://coriolis.io/schemas/ship-loadout/"},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0029",
        name=[{"@en": "JSON Web Token (JWT)"}],
        archive_team="http://fileformats.archiveteam.org/wiki/JSON_Web_Tokens",
        rfc="https://datatracker.ietf.org/doc/html/rfc7519",
        markers=[
            {"KEY": "alg", "EXISTS": None},
            {"KEY": "typ", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0030",
        name=[{"@en": "JHOVE JhoveView Output (generic)"}],
        markers=[
            {"GOTO": "jhove", "KEY": "name", "IS": "JhoveView"},
            {"GOTO": "jhove", "KEY": "release", "EXISTS": None},
            {"GOTO": "jhove", "KEY": "repInfo", "EXISTS": None},
        ],
    ),
    # JSON RPC uses three different keys, error, method, result. JSONID
    # Isn't expressive enough to test three keys in one go yet.
    registry_class.RegistryEntry(
        identifier="jrid:0031",
        name=[{"@en": "JSON RPC 2.0 (error)"}],
        markers=[
            {"KEY": "jsonrpc", "IS": "2.0"},
            {"KEY": "error", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0032",
        name=[{"@en": "JSON RPC 2.0 (request)"}],
        markers=[
            {"KEY": "jsonrpc", "IS": "2.0"},
            {"KEY": "method", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0033",
        name=[{"@en": "JSON RPC 2.0 (response)"}],
        markers=[
            {"KEY": "jsonrpc", "IS": "2.0"},
            {"KEY": "result", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0034",
        name=[{"@en": "Jupyter Notebook (Generic)"}],
        pronom="http://www.nationalarchives.gov.uk/PRONOM/fmt/1119",
        wikidata="http://www.wikidata.org/entity/Q105099901",
        archive_team="http://fileformats.archiveteam.org/wiki/Jupyter_Notebook",
        markers=[
            {"KEY": "metadata", "ISTYPE": dict},
            {"KEY": "nbformat", "ISTYPE": int},
            {"KEY": "nbformat_minor", "ISTYPE": int},
            {"KEY": "cells", "ISTYPE": list},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0035",
        name=[{"@en": "CSV Dialect Description Format (CDDF) (Generic)"}],
        archive_team="http://fileformats.archiveteam.org/wiki/CSV_Dialect_Description_Format",
        markers=[
            {"KEY": "csvddf_version", "EXISTS": None},
            {"GOTO": "dialect", "KEY": "delimiter", "EXISTS": None},
            {"GOTO": "dialect", "KEY": "doublequote", "EXISTS": None},
            {"GOTO": "dialect", "KEY": "lineterminator", "EXISTS": None},
            {"GOTO": "dialect", "KEY": "quotechar", "EXISTS": None},
            {"GOTO": "dialect", "KEY": "skipinitialspace", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0036",
        name=[{"@en": "CSV Dialect Description Format (CDDF) (1.2 - 1.x)"}],
        version="1.2",
        archive_team="http://fileformats.archiveteam.org/wiki/CSV_Dialect_Description_Format",
        markers=[
            {"KEY": "csvddfVersion", "EXISTS": None},
            {"KEY": "delimiter", "EXISTS": None},
            {"KEY": "doubleQuote", "EXISTS": None},
            {"KEY": "lineTerminator", "EXISTS": None},
            {"KEY": "quoteChar", "EXISTS": None},
            {"KEY": "skipInitialSpace", "EXISTS": None},
            {"KEY": "header", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0037",
        name=[{"@en": "GeoJSON Feature Object"}],
        archive_team="http://fileformats.archiveteam.org/wiki/GeoJSON",
        rfc="https://datatracker.ietf.org/doc/html/rfc7946",
        loc="https://www.loc.gov/preservation/digital/formats/fdd/fdd000382.shtml",
        wikidata="http://www.wikidata.org/entity/Q5533904",
        mime="application/vnd.geo+json",
        markers=[
            {"KEY": "type", "IS": "Feature"},
            {"KEY": "geometry", "EXISTS": None},
            {"KEY": "properties", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0038",
        name=[{"@en": "GeoJSON Feature Collection Object"}],
        archive_team="http://fileformats.archiveteam.org/wiki/GeoJSON",
        loc="https://www.loc.gov/preservation/digital/formats/fdd/fdd000382.shtml",
        rfc="https://datatracker.ietf.org/doc/html/rfc7946",
        mime="application/vnd.geo+json",
        markers=[
            {"KEY": "type", "IS": "FeatureCollection"},
            {"KEY": "features", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0039",
        name=[{"@en": "HAR (HTTP Archive) (Generic)"}],
        archive_team="http://fileformats.archiveteam.org/wiki/HAR",
        wikidata="http://www.wikidata.org/entity/Q13422998",
        markers=[
            {"GOTO": "log", "KEY": "version", "ISTYPE": str},
            {"GOTO": "log", "KEY": "creator", "ISTYPE": dict},
            {"GOTO": "log", "KEY": "entries", "ISTYPE": list},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0040",
        name=[{"@en": "JSON API"}],
        archive_team="http://fileformats.archiveteam.org/wiki/JSON_API",
        mime="application/vnd.api+json",
        markers=[
            # "jsonapi" MAY exist but isn't guaranteed. It is unlikely
            # we will see this object as a static document.
            {"KEY": "jsonapi", "ISTYPE": dict},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0041",
        name=[{"@en": "Max (Interactive Software) .maxpat JSON (Generic)"}],
        archive_team="http://fileformats.archiveteam.org/wiki/Max",
        wikidata="http://www.wikidata.org/entity/Q105862509",
        markers=[
            {"GOTO": "patcher", "KEY": "fileversion", "EXISTS": None},
            {"GOTO": "patcher", "KEY": "appversion", "ISTYPE": dict},
            {"GOTO": "patcher", "KEY": "bglocked", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0042",
        name=[{"@en": "Open Web App Manifest (Firefox Marketplace)"}],
        archive_team="http://fileformats.archiveteam.org/wiki/Open_Web_App_Manifest",
        mime="application/x-web-app-manifest+json",
        markers=[
            {"KEY": "name", "ISTYPE": str},
            {"KEY": "description", "ISTYPE": str},
            {"KEY": "icons", "ISTYPE": dict},
            {"GOTO": "developer", "KEY": "name", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0043",
        name=[{"@en": "PiskelApp Canvas (Generic)"}],
        archive_team="http://fileformats.archiveteam.org/wiki/Piskel_canvas",
        markers=[
            {"KEY": "modelVersion", "ISTYPE": int},
            {"GOTO": "piskel", "KEY": "name", "EXISTS": None},
            {"GOTO": "piskel", "KEY": "description", "EXISTS": None},
            {"GOTO": "piskel", "KEY": "layers", "ISTYPE": list},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0044",
        name=[{"@en": "Apple PassKit (PKPass) pass.json"}],
        archive_team="http://fileformats.archiveteam.org/wiki/PKPass",
        mime="application/vnd.apple.pkpass",
        markers=[
            {"KEY": "passTypeIdentifier", "EXISTS": None},
            {"KEY": "formatVersion", "ISTYPE": int},
            {"KEY": "serialNumber", "EXISTS": None},
            {"KEY": "teamIdentifier", "EXISTS": None},
            {"KEY": "organizationName", "EXISTS": None},
            {"KEY": "description", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0045",
        name=[{"@en": "Scratch Visual Programming Language - project.json"}],
        version="3.0",
        markers=[
            {"KEY": "targets", "ISTYPE": list},
            {"KEY": "meta", "EXISTS": None},
            {"GOTO": "meta", "KEY": "semver", "IS": "3.0.0"},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0046",
        name=[{"@en": "Scratch Visual Programming Language - project.json"}],
        version="2.0",
        archive_team="http://fileformats.archiveteam.org/wiki/Scratch_2.0_File_Format",
        markers=[
            {"KEY": "objName", "EXISTS": None},
            {"KEY": "costumes", "EXISTS": None},
            {"KEY": "children", "EXISTS": None},
            {"KEY": "penLayerMD5", "EXISTS": None},
            {"KEY": "info", "EXISTS": None},
            {"GOTO": "info", "KEY": "userAgent", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0047",
        name=[{"@en": "Sketch project file meta.json (Generic)"}],
        archive_team="http://fileformats.archiveteam.org/wiki/Sketch",
        mime="application/vnd.apple.pkpass",
        markers=[
            {"KEY": "commit", "EXISTS": None},
            {"KEY": "pagesAndArtboards", "ISTYPE": dict},
            {"KEY": "appVersion", "EXISTS": None},
            {"KEY": "build", "EXISTS": None},
            {"KEY": "created", "ISTYPE": dict},
        ],
    ),
    # Datapackage.org Schemas.
    registry_class.RegistryEntry(
        identifier="jrid:0048",
        name=[
            {"@en": "Data Package Schema (Datapackage.org (Open Knowledge Foundation))"}
        ],
        markers=[
            {"KEY": "$schema", "STARTSWITH": "http://json-schema.org/"},
            {"KEY": "$schema", "ENDSWITH": "/schema#"},
            {"KEY": "title", "IS": "Data Package"},
            {"KEY": "type", "IS": "object"},
            {"KEY": "required", "ISTYPE": list},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0049",
        name=[
            {
                "@en": "Data Package Resource Schema (Datapackage.org (Open Knowledge Foundation))"
            }
        ],
        markers=[
            {"KEY": "$schema", "STARTSWITH": "http://json-schema.org/"},
            {"KEY": "$schema", "ENDSWITH": "/schema#"},
            {"KEY": "title", "IS": "Data Resource"},
            {"KEY": "type", "IS": "object"},
            {"KEY": "oneOf", "ISTYPE": list},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0050",
        name=[
            {
                "@en": "Data Package Table Dialect (Datapackage.org (Open Knowledge Foundation))"
            }
        ],
        markers=[
            {"KEY": "$schema", "STARTSWITH": "http://json-schema.org/"},
            {"KEY": "$schema", "ENDSWITH": "/schema#"},
            {"KEY": "title", "IS": "Table Dialect"},
            {"KEY": "type", "IS": "object"},
            {"KEY": "properties", "ISTYPE": dict},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0051",
        name=[
            {
                "@en": "Data Package Table Schema (Datapackage.org (Open Knowledge Foundation))"
            }
        ],
        markers=[
            {"KEY": "$schema", "STARTSWITH": "http://json-schema.org/"},
            {"KEY": "$schema", "ENDSWITH": "/schema#"},
            {"KEY": "title", "IS": "Table Schema"},
            {"KEY": "type", "IS": ["string", "object"]},
            {"KEY": "required", "ISTYPE": list},
        ],
    ),
    # iPuz puzzles.
    registry_class.RegistryEntry(
        identifier="jrid:0052",
        name=[{"@en": "ipuz: open format for puzzles"}],
        archive_team="http://fileformats.archiveteam.org/wiki/IPUZ",
        wikidata="http://www.wikidata.org/entity/Q105857590",
        markers=[
            {"KEY": "version", "STARTSWITH": "http://ipuz.org/"},
            {"KEY": "kind", "ISTYPE": list},
            {"KEY": "puzzle", "ISTYPE": list},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0053",
        name=[{"@en": "SNIA Self-contained Information Retention Format (SIRF)"}],
        loc="https://www.loc.gov/preservation/digital/formats/fdd/fdd000584.shtml",
        wikidata="http://www.wikidata.org/entity/Q29905354",
        markers=[
            {"KEY": "catalogId", "EXISTS": None},
            {"KEY": "containerInformation", "EXISTS": None},
            {"KEY": "objectsSet", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0054",
        name=[{"@en": "Firefox Bookmarks Backup File"}],
        archive_team="http://fileformats.archiveteam.org/wiki/Firefox_bookmarks",
        wikidata="http://www.wikidata.org/entity/Q105857338",
        markers=[
            {"KEY": "guid", "EXISTS": None},
            {"KEY": "title", "EXISTS": None},
            {"KEY": "index", "ISTYPE": int},
            {"KEY": "dateAdded", "ISTYPE": int},
            {"KEY": "lastModified", "ISTYPE": int},
            {"KEY": "id", "ISTYPE": int},
            {"KEY": "typeCode", "ISTYPE": int},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0055",
        name=[{"@en": "Lottie vector graphics"}],
        archive_team="http://fileformats.archiveteam.org/wiki/Lottie",
        wikidata="http://www.wikidata.org/entity/Q98855048",
        markers=[
            {"KEY": "h", "EXISTS": None},
            {"KEY": "w", "EXISTS": None},
            {"KEY": "assets", "ISTYPE": list},
            {"KEY": "layers", "ISTYPE": list},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0056",
        name=[{"@en": "Camtasia TSCPROJ file"}],
        markers=[
            {"KEY": "title", "EXISTS": None},
            {"KEY": "description", "EXISTS": None},
            {"KEY": "author", "EXISTS": None},
            {"KEY": "height", "ISTYPE": float},
            {"KEY": "width", "ISTYPE": float},
            {"GOTO": "authoringClientName", "KEY": "name", "EXISTS": None},
            {"KEY": "metadata", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0057",
        name=[{"@en": "Grafana Dashboard Configuration"}],
        markers=[
            {"KEY": "uid", "ISTYPE": str},
            {"KEY": "title", "ISTYPE": str},
            {"KEY": "tags", "ISTYPE": list},
            {"KEY": "schemaVersion", "ISTYPE": int},
            {"KEY": "version", "ISTYPE": int},
            {"KEY": "panels", "ISTYPE": list},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0058",
        name=[{"@en": "Power Bi DataModelSchema"}],
        markers=[
            {"KEY": "name", "ISTYPE": str},
            {"KEY": "compatibilityLevel", "ISTYPE": int},
            {"GOTO": "model", "KEY": "defaultPowerBIDataSourceVersion", "ISTYPE": str},
        ],
    ),
]


def registry() -> list[registry_class.RegistryEntry]:
    """Return a registry object to the caller."""
    return _registry
