"""WSDL PARSER
Parsers for the WSDL API external data source.
"""

# # Installed # #
from bs4 import BeautifulSoup

# # Parent Package # #
from ..exceptions import ParseError, ParsingExceptions
from ..string_fixes import fix_stop_name

# # Project # #
from ...entities import Stop

__all__ = ("parse_xml_stop", "parse_xml_error_stop_not_exist")


def parse_xml_stop(content: str) -> Stop:
    """Parse the XML content returned after requesting the WSDL API Stop endpoint, and parse the Stop info.
    Unlike on the HTML dats source, when a not-existing Stop is queried on the WSDL API, the API returns an error;
    the StopNotExist exception is raised on the 'wsdl_request' module, helped by 'parse_xml_error_stop_not_exist'.
    :param content: XML response
    :raises: vigobus_getters.exceptions.ParseError
    """
    try:
        xml = BeautifulSoup(content, "lxml")
        stop_data = xml.find("Parada") or xml.find("parada")
        stop_id = int(stop_data["idparada"])
        stop_original_name = stop_data["nombre"]
        stop_name = fix_stop_name(stop_original_name)
        stop_lat = stop_data.get("latitud")
        stop_lon = stop_data.get("longitud")
        if stop_lat and stop_lon:
            stop_lat, stop_lon = float(stop_lat), float(stop_lon)

        return Stop(
            stop_id=stop_id,
            name=stop_name,
            original_name=stop_original_name,
            lat=stop_lat,
            lon=stop_lon
        )

    except ParsingExceptions:
        raise ParseError()


def parse_xml_error_stop_not_exist(content: str) -> bool:
    """When a call to the WSDL API is unsuccessful, the response text must be fed to this method in order to check
    if the error was caused because the Stop not exists.
    Returns True if the Stop NOT EXISTS, and False if that was not the problem which caused the request to fail.
    """
    return "No hay ninguna fila en la posición" in content


# def parse_xml_buses(content: str) -> List[Bus]:
#     try:
#         xml = BeautifulSoup(content, "lxml")
#         # API ENDPOINT is DOWN
#
#     except ParsingExceptions:
#         raise ParseError()
