from pathlib import Path
from xml.etree import ElementTree


def main() -> int:
    project_root = Path.cwd().resolve()
    report_path = project_root / "coverage.xml"

    try:
        report = ElementTree.parse(report_path)
    except (ElementTree.ParseError, OSError) as error:
        print(f"Unable to read {report_path}: {error}")
        return 1

    filenames = [
        class_element.get("filename", "")
        for class_element in report.findall(".//class")
    ]
    errors = []

    if not filenames:
        errors.append("coverage.xml does not contain any measured source file")

    for filename in filenames:
        relative_path = Path(filename)
        if not filename:
            errors.append("coverage.xml contains an empty source filename")
            continue
        if relative_path.is_absolute():
            errors.append(f"{filename}: expected a project-relative path")
            continue

        resolved_path = (project_root / relative_path).resolve()
        try:
            resolved_path.relative_to(project_root)
        except ValueError:
            errors.append(f"{filename}: resolves outside the project")
            continue

        if not resolved_path.is_file():
            errors.append(f"{filename}: does not resolve to a project file")

    if errors:
        print("Invalid coverage paths:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(filenames)} project-relative coverage paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
