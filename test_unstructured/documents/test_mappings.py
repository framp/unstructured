from collections import defaultdict
from typing import Type

from unstructured.documents import elements, ontology
from unstructured.documents.mappings import (
    ALL_ONTOLOGY_ELEMENT_TYPES,
    HTML_TAG_TO_DEFAULT_ELEMENT_TYPE_MAP,
    ONTOLOGY_CLASS_TO_UNSTRUCTURED_ELEMENT_TYPE,
    get_all_subclasses,
)
from unstructured.documents.ontology import OntologyElement


def test_if_all_html_tags_has_default_to_ontology_types():
    html_tag_to_allowed_tags: dict[str, list[Type[ontology.OntologyElement]]] = defaultdict(list)

    for element_type in ALL_ONTOLOGY_ELEMENT_TYPES:
        for tag in element_type().allowed_tags:
            html_tag_to_allowed_tags[tag].append(element_type)

    for html_tag, allowed_ontology_classes in html_tag_to_allowed_tags.items():
        assert html_tag in HTML_TAG_TO_DEFAULT_ELEMENT_TYPE_MAP
        assert HTML_TAG_TO_DEFAULT_ELEMENT_TYPE_MAP[html_tag] in allowed_ontology_classes + [
            ontology.UncategorizedText
        ]  # In some cases it is better to use unknown type than assign incorrect type


def test_all_expected_ontology_types_are_subclasses_of_OntologyElement():
    for element_type in HTML_TAG_TO_DEFAULT_ELEMENT_TYPE_MAP.values():
        assert issubclass(element_type, OntologyElement)


def test_ontology_to_unstructured_mapping_has_valid_types():
    for (
        ontology_element,
        unstructured_element,
    ) in ONTOLOGY_CLASS_TO_UNSTRUCTURED_ELEMENT_TYPE.items():
        assert issubclass(unstructured_element, elements.Element)
        assert issubclass(ontology_element, ontology.OntologyElement)


def test_all_ontology_elements_are_defined_in_mapping_to_unstructured():
    for ontology_element in get_all_subclasses(ontology.OntologyElement):
        assert ontology_element in ONTOLOGY_CLASS_TO_UNSTRUCTURED_ELEMENT_TYPE
