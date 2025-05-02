"""Code helperrs."""

import logging
import time

try:
    import htm_template
    import registry_data
except ModuleNotFoundError:
    try:
        from src.jsonid import htm_template, registry_data
    except ModuleNotFoundError:
        from jsonid import htm_template, registry_data


logger = logging.getLogger(__name__)


def _function_name(func: str) -> str:
    """Attemptt to retrieve function name for timeit."""
    return str(func).rsplit("at", 1)[0].strip().replace("<function", "def ").strip()


def timeit(func):
    """Decorator to output the time taken for a function"""

    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        func_name = _function_name(str(func)).strip()
        # pylint: disable=W1203
        logger.debug(f"Time taken: {elapsed:.6f} seconds ({func_name}())")
        return result

    return wrapper


def entry_check() -> bool:
    """Make sure the entries are all unique."""
    data = registry_data.registry()
    ids = [datum.identifier for datum in data]
    return len(set(ids)) == len(data)


def html():
    """Output HTML that can be used for documentation.

    Table e.g.

    ```htm
        <table>
            <tbody>
                <tr>
                    <th>id</th>
                    <th>name</th>
                    <th>pronom</th>
                    <th>wikidata</th>
                    <th>archiveteam</th>
                    <th>markers</th>
                </tr>
                <tr>
                    <td>a</td>
                    <td>b</td>
                    <td>c</td>
                    <td>d</td>
                    <td>e</td>
                    <td>f</td>
                </tr>
            </tbody>
        </table>
    ```

    List example:

    ```htm
        <li><code><a href="#">item.1</a></code></li>
        <li><code><a href="#">item.2</a></code></li>
        <li><code><a href="#">item.3</a></code></li>
    ```

    <a href="#div_id">jump link</a>

    """

    # pylint: disable=R0914

    data = registry_data.registry()
    content = """
        <tr>
            <td id="{id}">{id}</td>
            <td class="markers">{name}</td>
            <td>{pronom}</td>
            <td>{loc}</td>
            <td>{wikidata}</td>
            <td>{archiveteam}</td>
            <td class="markers">{markers}</td>
        </tr>
    """
    marker_snippet = """
        <pre>{marker_text}</pre>
    """
    list_snippet = """
        <li class="contents"><code><a href="#{id}">{id}: {name}</a></code></li>
    """
    content_arr = []
    list_arr = []
    for datum in data:
        id_ = datum.identifier
        name = datum.name[0]["@en"]
        pronom = datum.pronom != ""
        wikidata = datum.wikidata != ""
        archiveteam = datum.archive_team != ""
        loc = datum.loc != ""
        marker_text = ""
        for marker in datum.markers:
            marker_text = f"{marker_text}{marker}\n"
        row = content.format(
            id=id_,
            name=name,
            pronom=pronom,
            wikidata=wikidata,
            archiveteam=archiveteam,
            loc=loc,
            markers=marker_snippet.strip().format(marker_text=marker_text),
        )
        list_item = list_snippet.strip().format(id=id_, name=name)
        content_arr.append(row)
        list_arr.append(list_item)
    table = """
        <br>
        <table>
            <tbody>
                <tr>
                    <th>id</th>
                    <th>name</th>
                    <th>pronom</th>
                    <th>loc</th>
                    <th>wikidata</th>
                    <th>archiveteam</th>
                    <th>markers</th>
                </tr>
                {rows}
            </tbody>
        </table>
    """
    table = table.format(rows="".join(content_arr))
    table = table.strip()
    print(
        htm_template.HTM_TEMPLATE.replace("{{%%REGISTRY-DATA%%}}", table, 1).replace(
            "{{%%LIST-DATA%%}}", "".join(list_arr), 1
        )
    )
