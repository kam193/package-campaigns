import sys
import jinja2
import os
import json

CAMPAIGN_PAGES = "docs/pypi/campaign"
CAMPAIGN_PAGES_TEMPLATE = "templates/pypi-campaign.md.j2"
ABUSE_PAGES = "docs/pypi/abuse_category"
PACKAGE_PAGES = "docs/pypi/package"
PYPI_INDEX = "docs/pypi/index.md"

CAMPAIGN_JSONS = "pypi/campaigns"
PACKAGE_JSON = "pypi/packages"

ABUSE_JSON = "scripts/abuse.json"
CATEGORIES_JSON = "scripts/categories.json"

STATS = {
    "campaigns": [],
    "categories": {},
    "last_packages": [],
}


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
                    if campaign["category"] not in STATS["categories"]:
                        STATS["categories"][campaign["category"]] = {
                            "campaigns": 0,
                            "packages": 0,
                        }
                    STATS["categories"][campaign["category"]]["campaigns"] += 1
                    if "created_at" in campaign:
                        STATS["campaigns"].append(
                            (
                                campaign["created_at"],
                                campaign["name"].strip(),
                                campaign["category"],
                            )
                        )

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
                        STATS["categories"][campaigns[campaign_name]["category"]][
                            "packages"
                        ] += 1
                        if "campaign_assigned_at" in package:
                            STATS["last_packages"].append(
                                (
                                    package["campaign_assigned_at"],
                                    package["name"].strip(),
                                    campaign_name,
                                    campaigns[campaign_name]["category"],
                                )
                            )


def generate_pypi_index():
    newest_campaigns = sorted(STATS["campaigns"], key=lambda x: x[0], reverse=True)[:10]
    category_stats = sorted(
        STATS["categories"].items(), key=lambda x: x[0], reverse=False
    )
    last_packages = sorted(STATS["last_packages"], key=lambda x: x[0], reverse=True)[
        :10
    ]
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."))
    template = env.get_template("templates/pypi-index.md.j2")

    output = template.render(
        campaigns=newest_campaigns,
        categories=category_stats,
        last_packages=last_packages,
    )
    # Write the output to a file
    output_file = os.path.join(PYPI_INDEX)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as out_f:
        out_f.write(output)


if __name__ == "__main__":
    cpgs = generate_campaign_pages(limit=20 if "--test" in sys.argv else None)
    generate_packages(cpgs, limit=20 if "--test" in sys.argv else None)
    generate_pypi_index()
