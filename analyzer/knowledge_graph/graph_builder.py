import networkx as nx


def create_repository_graph() -> nx.DiGraph:
    """
    Create a directed repository knowledge graph.

    Nodes represent software entities.
    Edges represent relationships between entities.
    """

    return nx.DiGraph()


def add_file_node(
    graph: nx.DiGraph,
    file_path: str,
    language: str | None = None
) -> None:
    """
    Add a source-code file as a graph node.
    """

    graph.add_node(
        file_path,
        type="file",
        language=language
    )


def add_entity_node(
    graph: nx.DiGraph,
    entity_id: str,
    entity_type: str,
    name: str,
    file_path: str,
    start_line: int | None = None,
    end_line: int | None = None
) -> None:
    """
    Add a function, class, or other software entity
    as a graph node.
    """

    graph.add_node(
        entity_id,
        type=entity_type,
        name=name,
        file=file_path,
        startLine=start_line,
        endLine=end_line
    )


def add_relationship(
    graph: nx.DiGraph,
    source: str,
    target: str,
    relationship_type: str,
    **attributes
) -> None:
    """
    Add a directed relationship between two nodes.
    """

    graph.add_edge(
        source,
        target,
        type=relationship_type,
        **attributes
    )


def build_graph_from_ast(
    ast_results: dict
) -> nx.DiGraph:
    """
    Build a repository knowledge graph from AST analysis results.
    """

    graph = create_repository_graph()

    for file_path, result in ast_results.items():

        if not result.get("supported", False):
            continue

        language = result.get(
            "language"
        )

        # -------------------------
        # File Node
        # -------------------------

        add_file_node(
            graph,
            file_path,
            language
        )

        # -------------------------
        # Function Nodes
        # -------------------------

        functions = result.get(
            "functions",
            {}
        )

        for function_group in [
            "added",
            "deleted",
            "modified",
            "unchanged"
        ]:

            entities = functions.get(
                function_group,
                []
            )

            for function in entities:

                if isinstance(
                    function,
                    str
                ):
                    name = function
                    start_line = None
                    end_line = None

                else:
                    name = function.get(
                        "name",
                        "anonymous"
                    )

                    start_line = function.get(
                        "startLine"
                    )

                    end_line = function.get(
                        "endLine"
                    )

                entity_id = (
                    f"{file_path}::"
                    f"function::"
                    f"{name}"
                )

                add_entity_node(
                    graph,
                    entity_id,
                    "function",
                    name,
                    file_path,
                    start_line,
                    end_line
                )

                add_relationship(
                    graph,
                    file_path,
                    entity_id,
                    "CONTAINS"
                )

        # -------------------------
        # Class Nodes
        # -------------------------

        classes = result.get(
            "classes",
            {}
        )

        for class_group in [
            "added",
            "deleted",
            "modified",
            "unchanged"
        ]:

            entities = classes.get(
                class_group,
                []
            )

            for class_entity in entities:

                if isinstance(
                    class_entity,
                    str
                ):
                    name = class_entity
                    start_line = None
                    end_line = None

                else:
                    name = class_entity.get(
                        "name",
                        "anonymous"
                    )

                    start_line = class_entity.get(
                        "startLine"
                    )

                    end_line = class_entity.get(
                        "endLine"
                    )

                entity_id = (
                    f"{file_path}::"
                    f"class::"
                    f"{name}"
                )

                add_entity_node(
                    graph,
                    entity_id,
                    "class",
                    name,
                    file_path,
                    start_line,
                    end_line
                )

                add_relationship(
                    graph,
                    file_path,
                    entity_id,
                    "CONTAINS"
                )

    return graph

def add_repository_ast_to_graph(
    graph: nx.DiGraph,
    ast_results: dict
) -> None:
    """
    Add complete repository AST information
    into the knowledge graph.
    """

    for file_path, result in ast_results.items():

        if not result.get("supported", False):
            continue

        language = result.get(
            "language"
        )

        add_file_node(
            graph,
            file_path,
            language
        )

        # -------------------------
        # Functions
        # -------------------------

        for function in result.get(
            "functions",
            []
        ):

            name = function.get(
                "name",
                "anonymous"
            )

            entity_id = (
                f"{file_path}::"
                f"function::"
                f"{name}"
            )

            add_entity_node(
                graph,
                entity_id,
                "function",
                name,
                file_path,
                function.get("startLine"),
                function.get("endLine")
            )

            add_relationship(
                graph,
                file_path,
                entity_id,
                "CONTAINS"
            )

        # -------------------------
        # Classes
        # -------------------------

        for class_entity in result.get(
            "classes",
            []
        ):

            name = class_entity.get(
                "name",
                "anonymous"
            )

            entity_id = (
                f"{file_path}::"
                f"class::"
                f"{name}"
            )

            add_entity_node(
                graph,
                entity_id,
                "class",
                name,
                file_path,
                class_entity.get("startLine"),
                class_entity.get("endLine")
            )

            add_relationship(
                graph,
                file_path,
                entity_id,
                "CONTAINS"
            )




"""
Graph Builder Module

Constructs directed Repository Knowledge Graph using NetworkX from extracted code dependencies.
"""
