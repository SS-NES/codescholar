"""Citation analyser module."""
import yaml
from pathlib import Path

from . import Analyser, AnalyserType
from ..report import Report, is_empty


VALID_ATTRS = [
    # A description of the software.
    'abstract',
    # The authors of the software (definitions.person, definitions.entity).
    'authors',
    # The CFF schema version.
    'cff-version',
    # The commit hash or revision number of the sofware version.
    'commit',
    # The contact person, group, company, etc. for the software.
    'contact',
    # The date the software has been released (YYYY-MM-DD).
    'date-released',
    # The DOI of the software.
    'doi',
    # The identifiers of the software (definitions.identifier).
    'identifiers',
    # Keywords that describe the work.
    'keywords',
    # The SPDX license identifier(s) (definitions.license-enum)
    'license',
    # The URL of the license text (only for non-standard licenses)
    'license-url',
    # A message to let users know what to do with the citation metadata.
    'message',
    # A reference to another work that should be cited instead of the software
    # itself (definitions.reference).
    'preferred-citation',
    # Reference(s) to other creative works (e.g., other software (dependencies),
    # or other research products that the software builds on)
    # (definitions.reference).
    'references',
    # The URL of the software or dataset in a repository (when the repository
    # is neither a source code repository nor a build artifact repository).
    'repository',
    # The URL of the work in a build artifact repository.
    'repository-artifact',
    # The URL of the work in a source code repository.
    'repository-code',
    # The name of the software.
    'title',
    # The type of work (software or dataset)
    'type',
    # The URL of a landing page for the software.
    'url',
    # The version of the software (definitions.version)
    'version',
]


class Citation(Analyser):
    """Citation analyser class."""

    @classmethod
    def get_type(cls) -> AnalyserType:
        """Returns analyser type."""
        return AnalyserType.CITATION


    @classmethod
    def get_name(cls) -> str:
        """Returns analyser name."""
        return "Citation"


    @classmethod
    def includes(cls, path: Path) -> list[str]:
        """Returns file and directory patterns to be included in the analysis.

        Args:
            path (Path): Path of the code base.

        Returns:
            List of file and directory patterns.
        """
        return [
            '/*.cff',
        ]


    @classmethod
    def analyse_file(cls, path: Path, report: Report) -> dict:
        """Analyses a citation file.

        Args:
            path (Path): Path of the citation file.
            report (Report): Analysis report.

        Returns:
            Dictionary of the analysis results.
        """
        # Read citation file
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = yaml.safe_load(file)

        except:
            report.add_issue(cls, "Invalid citation file.", path)
            return {}

        # Check citation file format version
        cff_version = content.get('cff-version')

        if not cff_version:
            report.add_issue(cls, "Invalid citation file.", path)

        elif cff_version != '1.2.0':
            report.add_warning(cls, f"Invalid citation file format version {cff_version}.", path)

        # Check if title is missing
        if 'title' not in content:
            report.add_issue(cls, "The citation file is missing the title.", path)

        # Check if authors are missing
        if 'authors' not in content:
            report.add_issue(cls, "The citation file is missing the authors.", path)

        # Process attributes
        metadata_keys = {
            'abstract': 'description',
            'date-released': 'date_released',
            'doi': 'doi',
            'keywords': 'keywords',
            'repository-code': 'repository_code',
            'title': 'name',
            'version': 'version',
            'license': 'license',
        }

        for key, val in content.items():
            if key not in VALID_ATTRS:
                report.add_issue(cls, f"Invalid citation file attribute {key}", path)
                continue

            if key == 'type' and val != 'software':
                report.add_issue(cls, "The type of work is not indicated as software.", path)

            if key == 'license' and content.get('license-url'):
                report.add_warning(cls, "License URL should be used only if there is no license identifier.")

            if key in metadata_keys:
                report.add_metadata(cls, metadata_keys[key], val, path)
