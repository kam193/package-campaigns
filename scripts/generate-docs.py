import sys
import jinja2
import os
import json

CAMPAIGN_PAGES = "docs/pypi/campaign"
CAMPAIGN_PAGES_TEMPLATE = "templates/pypi-campaign.md.j2"
ABUSE_PAGES = "docs/pypi/abuse_category"
PACKAGE_PAGES = "docs/pypi/package"

CAMPAIGN_JSONS = "pypi/campaigns"
PACKAGE_JSON = "pypi/packages"

ABUSE_JSON = "scripts/abuse.json"
CATEGORIES_JSON = "scripts/categories.json"

CATEGORIES = {"MALICIOUS": ""}


def generate_campaign_pages(limit=None):
    """Generate campaign pages from JSON files."""
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."))
    template = env.get_template(CAMPAIGN_PAGES_TEMPLATE)

    abuse_template = env.get_template("templates/pypi-abuse-category.md.j2")
    abuse_categories = {}
    refresh_abuse = False
    with open(ABUSE_JSON, "r") as f:
        abuse_categories = json.load(f)
    with open(CATEGORIES_JSON, "r") as f:
        categories = json.load(f)

    campaigns = {}

    generated = 0
    for root, dirs, files in os.walk(CAMPAIGN_JSONS):
        for file in files:
            if limit and generated >= limit:
                break
            if file.endswith(".json"):
                generated += 1
                with open(os.path.join(root, file), "r") as f:
                    campaign = json.load(f)
                    campaigns[campaign["name"].strip()] = campaign
                    # Generate the campaign page
                    output = template.render(
                        campaign=campaign,
                        abuse_categories=abuse_categories,
                        categories=categories,
                    )
                    # Write the output to a file
                    output_file = os.path.join(
                        CAMPAIGN_PAGES, f"{campaign['name'].strip()}.md"
                    )
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    with open(output_file, "w") as out_f:
                        out_f.write(output)

                    for abuse in campaign.get("abuse_categories", []):
                        if abuse not in abuse_categories:
                            refresh_abuse = True
                            abuse_categories[abuse] = {}

    if refresh_abuse:
        with open(ABUSE_JSON, "w") as f:
            json.dump(abuse_categories, f, indent=4)

    for abuse, data in abuse_categories.items():
        abuse = abuse.strip()
        abuse_path = os.path.join(ABUSE_PAGES, f"{abuse}.md")
        abuse_output = abuse_template.render(
            name=abuse,
            description=abuse_categories[abuse].get("description", ""),
            long_description=abuse_categories[abuse].get("long_description", ""),
            theme=abuse_categories[abuse].get("theme", "danger"),
        )
        os.makedirs(os.path.dirname(abuse_path), exist_ok=True)
        with open(abuse_path, "w") as out_f:
            out_f.write(abuse_output)

    return campaigns


def generate_packages(campaigns: dict, limit=None):
    """Generate packages from campaigns."""
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."))
    template = env.get_template("templates/pypi-package.md.j2")

    with open(ABUSE_JSON, "r") as f:
        abuse_categories = json.load(f)
    with open(CATEGORIES_JSON, "r") as f:
        categories = json.load(f)

    generated = 0
    for root, dirs, files in os.walk(PACKAGE_JSON):
        for file in files:
            if limit and generated >= limit:
                break
            if file.endswith(".json"):
                generated += 1
                with open(os.path.join(root, file), "r") as f:
                    package = json.load(f)
                    campaign_name = package.get("campaign", "").strip()
                    if campaign_name in campaigns:
                        # Generate the package page
                        output = template.render(
                            package=package,
                            campaign=campaigns[campaign_name],
                            abuse_categories=abuse_categories,
                            categories=categories,
                        )
                        # Write the output to a file
                        output_file = os.path.join(
                            PACKAGE_PAGES, f"{package['name'].strip()}.md"
                        )
                        os.makedirs(os.path.dirname(output_file), exist_ok=True)
                        with open(output_file, "w") as out_f:
                            out_f.write(output)


if __name__ == "__main__":
    cpgs = generate_campaign_pages(limit=20 if "--test" in sys.argv else None)
    generate_packages(cpgs, limit=20 if "--test" in sys.argv else None)
