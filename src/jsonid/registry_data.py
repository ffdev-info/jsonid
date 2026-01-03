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
        name=[{"@en": "JavaScript Package Lock"}],
        description=[{"@en": "describes an exact Node (NPM) module dependency tree"}],
        markers=[
            {"KEY": "name", "EXISTS": None},
            {"KEY": "lockfileVersion", "EXISTS": None},
            {"KEY": "packages", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0002",
        name=[{"@en": "OCFL Inventory (Generic)"}],
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
        name=[{"@en": "RO-Crate (Generic)"}],
        markers=[
            {"KEY": "@context", "STARTSWITH": "https://w3id.org/ro/crate/"},
            {"KEY": "@context", "ENDSWITH": "/context"},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0006",
        name=[{"@en": "RO-Crate (1.1)"}],
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
            {"KEY": "$schema", "ENDSWITH": "/schema"},
            {"KEY": "$defs", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0008",
        name=[{"@en": "IIIF Image API (all versions)"}],
        markers=[
            {"KEY": "@context", "STARTSWITH": "http://iiif.io/api/image/"},
            {"KEY": "@context", "ENDSWITH": "/context.json"},
            {"KEY": "type", "CONTAINS": "ImageService"},
            {"KEY": "protocol", "IS": "http://iiif.io/api/image"},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0009",
        name=[{"@en": "JSON-LD (Generic)"}],
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
        name=[{"@en": "Siegfried Identification Report (Generic)"}],
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
        name=[{"@en": "SPARQL Query Results (W3C) (Generic)"}],
        markers=[
            {"KEY": "head", "EXISTS": None},
            {"KEY": "results", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0014",
        name=[{"@en": "Wikidata Query Service Sparql Results (WDQS) (Generic)"}],
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
        name=[{"@en": "Activity Streams JSON (Generic)"}],
        wikidata="http://www.wikidata.org/entity/Q4677626",
        markers=[
            {"KEY": "@context", "STARTSWITH": "https://www.w3.org/ns/activitystreams"},
            {"KEY": "id", "EXISTS": None},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0017",
        name=[{"@en": "Open Resume Document"}],
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
        markers=[
            {"KEY": "$schema", "STARTSWITH": "http://json-schema.org/"},
            {"KEY": "$schema", "ENDSWITH": "/schema#"},
            {"KEY": "name", "IS": "Document"},
            {"KEY": "is", "IS": "http://largemind.com/schema/jacker-song-1#"},
            {"KEY": "namespace", "IS": "jacker"},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0019",
        name=[{"@en": "JSON Patch"}],
        mime=["application/json-patch+json"],
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
            {
                "@en": "GL Transmission Format: GLTF runtime 3D asset library schema (Generic)"
            }
        ],
        archive_team="http://fileformats.archiveteam.org/wiki/GlTF",
        markers=[
            {"KEY": "$schema", "STARTSWITH": "https://json-schema.org/"},
            {"KEY": "$schema", "ENDSWITH": "/schema"},
            {"KEY": "title", "EXISTS": None},
            {"KEY": "type", "IS": "object"},
            {"KEY": "description", "IS": "The root object for a glTF asset."},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0021",
        name=[{"@en": "Tweet Object"}],
        pronom="http://www.nationalarchives.gov.uk/PRONOM/fmt/1311",
        wikidata="http://www.wikidata.org/entity/Q85415600",
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
        name=[{"@en": "JavaScript Package file"}],
        description=[{"@en": "describes a Node (NPM) package for publication"}],
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
        name=[{"@en": "Parcore Schema Document"}],
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
        name=[{"@en": "JHOVE JhoveView Output (Generic)"}],
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
        mime=["application/vnd.geo+json"],
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
        mime=["application/vnd.geo+json"],
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
        mime=["application/vnd.api+json"],
        markers=[
            # "jsonapi" MAY exist but isn't guaranteed. It is unlikely
            # we will see this object as a static document.
            {"KEY": "jsonapi", "ISTYPE": dict},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0041",
        name=[{"@en": "Max Patch (Visual Programming Language) (Generic)"}],
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
        mime=["application/x-web-app-manifest+json"],
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
        mime=["application/vnd.apple.pkpass"],
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
        mime=["application/vnd.apple.pkpass"],
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
            {"KEY": "id", "ISTYPE": int},
            {"KEY": "children", "ISTYPE": list},
            {"KEY": "root", "IS": "placesRoot"},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0055",
        name=[{"@en": "Lottie vector graphics"}],
        description=[
            {"@en": "a animated file format using JSON also known as Bodymovin JSON"}
        ],
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
        name=[{"@en": "Power Bi Data Model Schema"}],
        markers=[
            {"KEY": "name", "ISTYPE": str},
            {"KEY": "compatibilityLevel", "ISTYPE": int},
            {"GOTO": "model", "KEY": "defaultPowerBIDataSourceVersion", "ISTYPE": str},
        ],
    ),
    # ImageMagick convert output could benefit from being able to
    # search one dictionary deeper as it looks like [{{"data": "???"}}]
    # and this proposed marker is probably quite weak, although it
    # does require an array and two keys.
    registry_class.RegistryEntry(
        identifier="jrid:0059",
        name=[{"@en": "ImageMagick Convert Output"}],
        markers=[
            {"INDEX": 0, "KEY": "version", "ISTYPE": str},
            {"INDEX": 0, "KEY": "image", "ISTYPE": dict},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0060",
        name=[{"@en": "JSON Entity Model Schema (Minecraft OptiFine)"}],
        wikidata="http://www.wikidata.org/entity/Q105857389",
        markers=[
            {"KEY": "$schema", "STARTSWITH": "http://json-schema.org"},
            {"KEY": "$schema", "ENDSWITH": "/schema"},
            {"KEY": "title", "IS": "Custom Entity Models Model"},
            {"KEY": "type", "IS": "object"},
            {"GOTO": "properties", "KEY": "models", "ISTYPE": dict},
            {"KEY": "required", "IS": ["models"]},
            {"KEY": "additionalProperties", "ISTYPE": bool},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0061",
        name=[{"@en": "JSON Entity Model (Minecraft OptiFine)"}],
        wikidata="http://www.wikidata.org/entity/Q105857389",
        markers=[
            {"KEY": "models", "ISTYPE": list},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0062",
        name=[{"@en": "JSON Playlist File (JSPF)"}],
        wikidata="http://www.wikidata.org/entity/Q105857388",
        markers=[
            {"GOTO": "playlist", "KEY": "title", "ISTYPE": str},
            {"GOTO": "playlist", "KEY": "track", "ISTYPE": list},
        ],
    ),
    # Example: https://github.com/readyplayerme/Lyra-Sample.
    registry_class.RegistryEntry(
        identifier="jrid:0063",
        name=[{"@en": "Unreal Engine Project (Generic)"}],
        wikidata="http://www.wikidata.org/entity/Q105856666",
        markers=[
            {"KEY": "FileVersion", "ISTYPE": int},
            {"KEY": "EngineAssociation", "ISTYPE": str},
            {"KEY": "Description", "ISTYPE": str},
            {"KEY": "Modules", "ISTYPE": list},
            {"KEY": "Plugins", "ISTYPE": list},
        ],
    ),
    # Examples also at:  https://github.com/readyplayerme/Lyra-Sample.
    registry_class.RegistryEntry(
        identifier="jrid:0064",
        name=[{"@en": "Unreal Engine Plugin (Generic)"}],
        wikidata="http://www.wikidata.org/entity/Q105856746",
        markers=[
            {"KEY": "FileVersion", "ISTYPE": int},
            {"KEY": "Version", "ISTYPE": int},
            {"KEY": "FriendlyName", "ISTYPE": str},
            {"KEY": "EnabledByDefault", "ISTYPE": bool},
            {"KEY": "MarketplaceURL", "ISTYPE": str},
            {"KEY": "DocsURL", "ISTYPE": str},
            {"KEY": "Modules", "ISTYPE": list},
            {"KEY": "Description", "ISTYPE": str},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0065",
        name=[{"@en": "Canadian Product Incident Report form"}],
        wikidata="http://www.wikidata.org/entity/Q105857241",
        markers=[
            {"KEY": "form", "ISTYPE": dict},
            {"GOTO": "form", "KEY": "formIdentifier", "EXISTS": None},
            {"KEY": "report", "ISTYPE": dict},
            {"KEY": "submission", "ISTYPE": dict},
            {"KEY": "submitter", "ISTYPE": dict},
            {"KEY": "product", "ISTYPE": dict},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0066",
        name=[{"@en": "QMK Firmware Keymap"}],
        wikidata="http://www.wikidata.org/entity/Q105857362",
        markers=[
            {"KEY": "version", "ISTYPE": int},
            {"KEY": "notes", "ISTYPE": str},
            {"KEY": "keymap", "ISTYPE": str},
            {"KEY": "keyboard", "ISTYPE": str},
            {"KEY": "layout", "ISTYPE": str},
            {"KEY": "layers", "ISTYPE": list},
            {"KEY": "author", "ISTYPE": str},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0067",
        name=[{"@en": "Trizbort.io Adventure Game Map"}],
        wikidata="http://www.wikidata.org/entity/Q105857377",
        markers=[
            {"GOTO": "settings", "KEY": "basic", "EXISTS": None},
            {"GOTO": "settings", "KEY": "grid", "EXISTS": None},
            {"KEY": "title", "ISTYPE": str},
            {"KEY": "author", "ISTYPE": str},
            {"KEY": "elements", "ISTYPE": list},
            {"KEY": "description", "ISTYPE": str},
            {"KEY": "startRoom", "ISTYPE": int},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0068",
        name=[{"@en": "Allotrope Simple Model (Allotrope Foundation)"}],
        wikidata="http://www.wikidata.org/entity/Q131232260",
        markers=[
            {
                "KEY": "$asm.manifest",
                "STARTSWITH": "http://purl.allotrope.org/manifests/",
            },
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0069",
        name=[{"@en": "Sublime Text Project"}],
        wikidata="http://www.wikidata.org/entity/Q105852854",
        # Ideally we would then identify the first dict in the list
        # as having key 'path'.
        markers=[
            {
                "KEY": "folders",
                "ISTYPE": list,
            },
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0070",
        name=[{"@en": "Sublime Text Workspace"}],
        wikidata="http://www.wikidata.org/entity/Q105851929",
        markers=[
            {"KEY": "auto_complete", "ISTYPE": dict},
            {"KEY": "buffers", "ISTYPE": list},
            {"KEY": "layout", "ISTYPE": dict},
            {"KEY": "project", "ISTYPE": str},
            {"KEY": "settings", "ISTYPE": dict},
            {"KEY": "status_bar_visible", "ISTYPE": bool},
            {"KEY": "side_bar_visible", "ISTYPE": bool},
            {"KEY": "show_tabs", "ISTYPE": bool},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0071",
        name=[{"@en": "Chrome Bookmarks"}],
        wikidata="http://www.wikidata.org/entity/Q105858840",
        archive_team="http://fileformats.archiveteam.org/wiki/Chrome_bookmarks",
        markers=[
            {"KEY": "checksum", "EXISTS": None},
            {"GOTO": "roots", "KEY": "bookmark_bar", "ISTYPE": dict},
            {"KEY": "version", "ISTYPE": int},
        ],
    ),
    # Asciicast / Ascinnema V1: JSON
    # ref: https://docs.asciinema.org/manual/asciicast/v1/
    registry_class.RegistryEntry(
        identifier="jrid:0072",
        name=[{"@en": "asciicast (asciinema.org) v1"}],
        markers=[
            {"KEY": "version", "ISTYPE": int},
            {"KEY": "width", "ISTYPE": int},
            {"KEY": "height", "ISTYPE": int},
            {"KEY": "duration", "ISTYPE": float},
            {"KEY": "command", "ISTYPE": str},
            {"KEY": "title", "ISTYPE": str},
            {"KEY": "env", "EXISTS": None},
            {"KEY": "stdout", "EXISTS": None},
        ],
    ),
    # MAME Plugins distributed with the project:
    # https://github.com/mamedev/mame/tree/134d5251a19f486bac79944f122e489d4b6cd6e7/plugins
    registry_class.RegistryEntry(
        identifier="jrid:0073",
        name=[{"@en": "MAME Plugin (JSON)"}],
        wikidata="http://www.wikidata.org/entity/Q105857365",
        archive_team="http://fileformats.archiveteam.org/wiki/MAME",
        markers=[
            {"GOTO": "plugin", "KEY": "name", "ISTYPE": str},
            {"GOTO": "plugin", "KEY": "description", "ISTYPE": str},
            {"GOTO": "plugin", "KEY": "version", "ISTYPE": str},
            {"GOTO": "plugin", "KEY": "author", "ISTYPE": str},
            {"GOTO": "plugin", "KEY": "type", "ISTYPE": str},
            {"GOTO": "plugin", "KEY": "start", "ISTYPE": str},
        ],
    ),
    # TopoJSON spec:
    # https://github.com/topojson/topojson-specification/blob/7939fe0834f36af8b935ec1827cb0abdd1e34d36/README.md#21-topology-objects
    #
    # Additional examples:
    # https://github.com/topojson/topojson-server/tree/a6b85929df5dfc3de06d2bb0a4507b76967ce899/test/topojson
    registry_class.RegistryEntry(
        identifier="jrid:0074",
        name=[{"@en": "TopoJSON (GeoJSON extension)"}],
        wikidata="http://www.wikidata.org/entity/Q15838827",
        markers=[
            {"KEY": "type", "IS": "Topology"},
            {"KEY": "objects", "ISTYPE": dict},
            {"KEY": "arcs", "ISTYPE": list},
        ],
    ),
    # CryEngine; CryProject file
    # https://github.com/search?q=cryproject&type=code
    registry_class.RegistryEntry(
        identifier="jrid:0075",
        name=[{"@en": "CryProject file for CryEngine"}],
        wikidata="http://www.wikidata.org/entity/Q105850591",
        markers=[
            {"KEY": "version", "ISTYPE": int},
            {"KEY": "type", "ISTYPE": str},
            {"KEY": "info", "ISTYPE": dict},
            {"KEY": "content", "ISTYPE": dict},
        ],
    ),
    # CSL language schemas.
    #
    # https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html#
    registry_class.RegistryEntry(
        identifier="jrid:0076",
        name=[{"@en": "Citation Style Language Citation (CSL-JSON) Schema"}],
        markers=[
            {"KEY": "$schema", "STARTSWITH": "http://json-schema.org/"},
            {"KEY": "$schema", "ENDSWITH": "/schema#"},
            {"KEY": "$id", "STARTSWITH": "https://resource.citationstyles.org/schema/"},
            {"KEY": "$id", "ENDSWITH": "/input/json/csl-citation.json"},
            {"KEY": "type", "IS": "object"},
            {"KEY": "properties", "ISTYPE": dict},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0077",
        name=[{"@en": "Citation Style Language Input Data Schema"}],
        markers=[
            {"KEY": "$schema", "STARTSWITH": "http://json-schema.org/"},
            {"KEY": "$schema", "ENDSWITH": "/schema#"},
            {"KEY": "$id", "STARTSWITH": "https://resource.citationstyles.org/schema/"},
            {"KEY": "$id", "ENDSWITH": "/input/json/csl-data.json"},
            {"KEY": "type", "IS": "array"},
            {"KEY": "items", "ISTYPE": dict},
            {"KEY": "definitions", "ISTYPE": dict},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0078",
        name=[
            {
                "@en": "Wikidata Query Service Sparql Results (Wikiprov/Siegfried) (Generic)"
            }
        ],
        markers=[
            {"KEY": "head", "EXISTS": None},
            {"KEY": "results", "EXISTS": None},
            {"KEY": "endpoint", "IS": "https://query.wikidata.org/sparql"},
            {"KEY": "provenance", "EXISTS": None},
        ],
    ),
    # Asciicast / Asciinema V2: JSONL
    # Ref: https://docs.asciinema.org/manual/asciicast/v2/
    registry_class.RegistryEntry(
        identifier="jrid:0079",
        name=[{"@en": "asciicast (asciinema.org) v2"}],
        markers=[
            {"KEY": "version", "ISTYPE": int},
            {"KEY": "width", "ISTYPE": int},
            {"KEY": "height", "ISTYPE": int},
        ],
    ),
    # Asciicast / Asciinema V3: JSONL
    # Ref: https://docs.asciinema.org/manual/asciicast/v3/
    registry_class.RegistryEntry(
        identifier="jrid:0080",
        name=[{"@en": "asciicast (asciinema.org) v3"}],
        markers=[
            {"KEY": "version", "ISTYPE": int},
            {"KEY": "term", "ISTYPE": dict},
        ],
    ),
]


def registry() -> list[registry_class.RegistryEntry]:
    """Return a registry object to the caller."""
    return _registry
