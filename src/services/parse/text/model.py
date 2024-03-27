from pydantic import Field
from typing import Optional

from parse.model import ParseFileRequest


class PartitionStrategy:
    AUTO = "auto"
    FAST = "fast"
    OCR_ONLY = "ocr_only"
    HI_RES = "hi_res"


class PDFParams(ParseFileRequest):
    strategy: str = Field(
        default=PartitionStrategy.AUTO,
        description="""The strategy to use for partitioning the PDF. Valid strategies are "hi_res",
        "ocr_only", and "fast". When using the "hi_res" strategy, the function uses
        a layout detection model to identify document elements. When using the
        "ocr_only" strategy, partition_pdf simply extracts the text from the
        document using OCR and processes it. If the "fast" strategy is used, the text
        is extracted directly from the PDF. The default strategy `auto` will determine
        when a page can be extracted using `fast` mode, otherwise it will fall back to `hi_res`.""",
    )
    infer_table_structure: Optional[bool] = Field(
        default=False,
        description="Applicable if strategy='hi_res'. If True, extracts tables with their structure preserved as HTML.",
    )
    hi_res_model_name: Optional[str] = Field(
        default=None,
        description="The layout detection model used when partitioning strategy is set to 'hi_res'.",
    )


class HTMLParams(ParseFileRequest):
    skip_headers_and_footers: Optional[bool] = Field(
        default=False,
        description="If True, ignores any content that is within <header> or <footer> tags",
    )


class CSVParams(ParseFileRequest):
    include_header: Optional[bool] = Field(
        default=False,
        description="Determines whether or not header info is included in text and medatada.text_as_html",
    )


class PPTParams(ParseFileRequest):
    pass


class PPTXParams(ParseFileRequest):
    pass


class XLSXParams(ParseFileRequest):
    include_header: Optional[bool] = Field(
        default=False,
        description="Determines whether or not header info is included in text and medatada.text_as_html",
    )
