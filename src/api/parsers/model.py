from pydantic import BaseModel, Field, root_validator
from typing import Optional, Annotated
from _exceptions import BadRequestError


class ParseFileRequest(BaseModel):
    # Common Parameters across Parsers
    file_url: Optional[str] = Field(
        default=None,
        description="URL of the file to be parsed. Either 'file_url' or 'contents' must be provided, but not both."
    )
    contents: Optional[str] = Field(
        default=None,
        description="Either 'file_url' or 'contents' must be provided, but not both."
    )
    should_chunk: Optional[bool] = True
    clean_text: Optional[bool] = True
    max_characters_per_chunk: Optional[int] = None

    # Parser specific Parameters
    class Config:
        extra = "allow"

    @root_validator(pre=True)
    def check_mutually_exclusive_fields(cls, values):
        file_url, contents = values.get("file_url", None), values.get(
            "contents", None
        )
        if file_url and contents:
            raise BadRequestError(
                error={
                    "message": "Only one of 'file_url' or 'contents' can be provided."
                }
            )
        if not file_url and not contents:
            raise BadRequestError(
                error={"message": "Either 'file_url' or 'contents' must be provided."}
            )
        return values


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


class XLSXParams(ParseFileRequest):
    include_header: Optional[bool] = Field(
        default=False,
        description="Determines whether or not header info is included in text and medatada.text_as_html",
    )
