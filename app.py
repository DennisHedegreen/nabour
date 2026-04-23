from __future__ import annotations

import streamlit as st

from cross_border_matcher import build_matcher_state, compute_cross_border_matches
from info_content import get_info
from income_conversion import income_to_home_currency_display
from pair_registry import get_pair_spec, get_target_country_id, list_pair_specs, pair_label
from region_metadata import get_region_navigation
from translations import DEFAULT_LANGUAGE, LANGUAGE_LABELS, SUPPORTED_LANGUAGES, country_label, factor_label, t


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #f4f5ef 0%, #eceee4 100%);
            color: #171b16;
        }
        .block-container {
            max-width: 760px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        .nabour-title {
            font-size: 2.35rem;
            letter-spacing: 0.02em;
            margin: 0;
            color: #171b16;
            text-align: center;
        }
        .nabour-topbar {
            background: rgba(255, 255, 250, 0.92);
            border: 1px solid rgba(23, 27, 22, 0.08);
            border-radius: 999px;
            min-height: 3.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.6rem;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.55);
        }
        .nabour-topbar-title {
            font-size: 1.05rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            color: #171b16;
            margin: 0;
        }
        .nabour-subtitle {
            color: #677063;
            font-size: 1rem;
            margin-top: 0.55rem;
            margin-bottom: 0;
            text-align: center;
        }
        .nabour-card {
            background: rgba(248, 250, 243, 0.92);
            border: 1px solid rgba(23, 27, 22, 0.10);
            border-radius: 18px;
            padding: 1rem 1rem 0.8rem 1rem;
            margin-bottom: 0.9rem;
        }
        .nabour-matchbar {
            background: rgba(255, 255, 250, 0.95);
            border: 1px solid rgba(23, 27, 22, 0.08);
            border-radius: 999px;
            min-height: 2.7rem;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 0.75rem;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5);
        }
        .nabour-matchbar-title {
            font-size: 0.98rem;
            font-weight: 700;
            letter-spacing: 0.01em;
            color: #171b16;
        }
        .nabour-meta {
            color: #5f6a5b;
            font-size: 0.92rem;
        }
        .nabour-score {
            font-size: 1.4rem;
            font-weight: 700;
            color: #1f6a38;
        }
        .nabour-factor-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 0.6rem;
            font-size: 0.94rem;
        }
        .nabour-factor-table th,
        .nabour-factor-table td {
            border-bottom: 1px solid rgba(23, 27, 22, 0.08);
            padding: 0.45rem 0.35rem;
            text-align: left;
        }
        .nabour-small {
            color: #677063;
            font-size: 0.88rem;
        }
        .nabour-bottom-note {
            margin-top: 1rem;
        }
        .nabour-factor-list {
            margin-top: 0.4rem;
        }
        .nabour-factor-block {
            padding: 0.15rem 0 0.95rem 0;
            margin-bottom: 0.8rem;
        }
        .nabour-factor-block--close {
            border-top: 2px solid rgba(103, 136, 92, 0.22);
        }
        .nabour-factor-block--mid {
            border-top: 2px solid rgba(164, 145, 98, 0.18);
        }
        .nabour-factor-block--far {
            border-top: 2px solid rgba(182, 138, 92, 0.20);
        }
        .nabour-factor-value {
            font-size: 1rem;
            font-weight: 700;
            color: #171b16;
            margin-top: 0.7rem;
            margin-bottom: 0.35rem;
        }
        .nabour-compare-name {
            color: #5f6a5b;
            font-size: 0.89rem;
            margin-bottom: 0.2rem;
        }
        .nabour-compare-diff {
            color: #4a5548;
            font-size: 0.94rem;
            margin-top: 0.2rem;
        }
        .nabour-figure {
            color: #171b16;
            font-weight: 700;
            font-size: 1.04em;
        }
        .nabour-detail-heading {
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #677063;
            margin-top: 0.2rem;
            margin-bottom: 0.5rem;
        }
        div[data-testid="stPopover"] {
            display: flex;
            justify-content: flex-end;
        }
        div[data-testid="stPopover"] > div > button {
            min-height: 2.5rem;
            width: 2.5rem;
            border-radius: 999px;
            padding: 0;
            font-size: 1.1rem;
            font-weight: 700;
            line-height: 1;
            border: 1px solid rgba(23, 27, 22, 0.12);
            background: rgba(255, 255, 250, 0.96);
            box-shadow: 0 6px 22px rgba(23, 27, 22, 0.08);
        }
        .stButton > button {
            width: 100%;
            border-radius: 16px;
            min-height: 4.25rem;
            padding: 1rem 1.1rem;
            border: 1px solid rgba(23, 27, 22, 0.14);
            background: rgba(250, 251, 246, 0.96);
            color: #171b16;
            font-weight: 600;
            font-size: 1.02rem;
        }
        .stButton > button:hover {
            border-color: rgba(31, 106, 56, 0.40);
            color: #1f6a38;
        }
        @media (max-width: 640px) {
            .block-container {
                padding-top: 1.2rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .nabour-title {
                font-size: 1.85rem;
            }
            .nabour-topbar {
                min-height: 3.1rem;
                margin-bottom: 1.2rem;
            }
            .nabour-factor-table {
                font-size: 0.86rem;
            }
            .stButton > button {
                min-height: 3.8rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def get_matcher_state(pair_id: str):
    return build_matcher_state(pair_id)


@st.cache_data
def get_region_maps(pair_id: str):
    pair_spec = get_pair_spec(pair_id)
    return {
        country_id: get_region_navigation(
            country_id,
            reference_year=pair_spec.reference_year,
            factor_keys=pair_spec.factor_keys,
            factor_years={factor_key: pair_spec.factor_year(country_id, factor_key) for factor_key in pair_spec.factor_keys},
        )
        for country_id in pair_spec.countries
    }


def get_language() -> str:
    return st.session_state.get("language", DEFAULT_LANGUAGE)


def get_selected_pair_id() -> str:
    return st.session_state.get("pair_id") or list_pair_specs(active_only=True)[0].pair_id


def render_settings_menu() -> None:
    language = get_language()
    pair_id = get_selected_pair_id()
    info = get_info(language, pair_id)
    with st.popover("⚙"):
        selected_language = st.selectbox(
            t(language, "language"),
            options=list(SUPPORTED_LANGUAGES),
            index=list(SUPPORTED_LANGUAGES).index(language),
            format_func=lambda code: LANGUAGE_LABELS[code],
            key="nabour-language-select",
        )
        st.session_state["language"] = selected_language
        language = selected_language
        pair_id = get_selected_pair_id()
        info = get_info(language, pair_id)
        pair_spec = get_pair_spec(pair_id)

        st.markdown(f"**{t(language, 'about_this_tool')}**")
        for line in info["about"]:
            st.markdown(f"- {line}")

        st.markdown(f"**{pair_label(language, pair_id)}**")
        st.markdown(f"- {t(language, 'pair_reference_year', year=pair_spec.reference_year)}")

        st.markdown(f"**{t(language, 'how_matching_works')}**")
        for line in info["method"]:
            st.markdown(f"- {line}")

        st.markdown(f"**{t(language, 'what_numbers_mean')}**")
        for english_label, explanation in info["factors"].items():
            st.markdown(f"- **{factor_label(language, english_label)}:** {explanation}")

        st.markdown(f"**{t(language, 'income_note')}**")
        st.markdown(info["income_note"])


def format_factor_value(label: str, value: float, country_id: str) -> str:
    if label == "Population":
        return f"{value:,.0f}"
    if label in {"Age 65+", "Education", "Turnout"}:
        return f"{value:,.1f}%"
    if label == "Population density":
        return f"{round(value):,} per km²"
    if label == "Cars":
        return f"{round(value):,} per 1,000 residents"
    if label == "Income":
        if country_id == "denmark":
            return f"{value:,.0f} DKK"
        if country_id == "sweden":
            return f"{value:,.1f} on Sweden's income scale"
        return f"{value:,.0f} NOK"
    return f"{value:,.1f}"


def round_estimate(value: float) -> int:
    absolute = abs(value)
    if absolute >= 10_000:
        return int(round(value / 1000.0) * 1000)
    if absolute >= 1_000:
        return int(round(value / 100.0) * 100)
    if absolute >= 100:
        return int(round(value / 10.0) * 10)
    return int(round(value))


def format_estimate(value: float) -> str:
    return f"{round_estimate(value):,}"


def figure(text: str) -> str:
    return f'<span class="nabour-figure">{text}</span>'


def get_factor_block_class(standardized_gap: float) -> str:
    if standardized_gap <= 0.45:
        return "nabour-factor-block nabour-factor-block--close"
    if standardized_gap <= 1.0:
        return "nabour-factor-block nabour-factor-block--mid"
    return "nabour-factor-block nabour-factor-block--far"


def reset_after_pair_change(pair_id: str) -> None:
    st.session_state["pair_id"] = pair_id
    st.session_state["source_country"] = None
    st.session_state["source_region"] = None
    st.session_state["source_municipality"] = None
    st.session_state["current_step"] = "country"


def reset_after_country_change(country_id: str) -> None:
    st.session_state["source_country"] = country_id
    st.session_state["source_region"] = None
    st.session_state["source_municipality"] = None
    st.session_state["current_step"] = "region"


def country_cta_label(language: str, country_id: str) -> str:
    key_map = {
        "denmark": "i_am_from_denmark",
        "sweden": "i_am_from_sweden",
        "norway": "i_am_from_norway",
    }
    return t(language, key_map[country_id])

def describe_difference(detail, source_name: str) -> str:
    diff = detail.target_value - detail.source_value
    if abs(diff) < 0.05:
        return f"Almost the same as in {source_name}."
    direction = "more" if diff > 0 else "less"
    amount = abs(diff)

    if detail.label == "Population":
        return f"That is about {round(amount):,} {direction} people than in {source_name}."
    if detail.label in {"Age 65+", "Education", "Turnout"}:
        return f"That is about {amount:.1f} percentage points {direction} than in {source_name}."
    if detail.label == "Population density":
        return f"That is about {round(amount):,} {direction} people per km² than in {source_name}."
    if detail.label == "Cars":
        return f"That is about {round(amount):,} {direction} cars per 1,000 residents than in {source_name}."
    if detail.label == "Income":
        return "Income is shown in each country's own unit, so this is not a direct money difference."
    return ""


def render_factor_comparison_block(
    source_name: str,
    source_country: str,
    match_name: str,
    match_country: str,
    detail,
    factor_lookup: dict[str, object],
) -> None:
    language = get_language()
    title = detail.label
    source_line = f"{source_name}: {format_factor_value(detail.label, detail.source_value, source_country)}"
    target_line = f"In {match_name}: {format_factor_value(detail.label, detail.target_value, match_country)}"
    diff_line = describe_difference(detail, source_name)
    note_line = ""

    if detail.label == "Population":
        diff = detail.target_value - detail.source_value
        direction = t(language, "more") if diff > 0 else t(language, "less")
        title = t(language, "population_people")
        source_line = t(language, "place_plain", place=source_name, value=figure(format_estimate(detail.source_value)))
        target_line = t(language, "in_place_about", place=match_name, value=figure(format_estimate(detail.target_value)))
        if abs(diff) < 1:
            diff_line = t(language, "almost_same_size")
        else:
            diff_line = t(language, "about_more_less", value=figure(format_estimate(abs(diff))), direction=direction)

    elif detail.label in {"Age 65+", "Education"}:
        population_detail = factor_lookup["Population"]
        source_count = population_detail.source_value * detail.source_value / 100.0
        target_count = population_detail.target_value * detail.target_value / 100.0
        diff = target_count - source_count
        direction = t(language, "more") if diff > 0 else t(language, "less")
        if detail.label == "Age 65+":
            title = t(language, "people_65_or_older")
        else:
            title = t(language, "people_with_higher_education")
        source_line = t(language, "in_place_about", place=source_name, value=figure(format_estimate(source_count)))
        target_line = t(language, "in_place_about", place=match_name, value=figure(format_estimate(target_count)))
        if abs(diff) < 1:
            diff_line = t(language, "almost_same")
        else:
            diff_line = t(language, "about_more_less", value=figure(format_estimate(abs(diff))), direction=direction)

    elif detail.label == "Income":
        home_currency, source_income = income_to_home_currency_display(
            source_country,
            detail.source_value,
            source_country,
        )
        _, target_income = income_to_home_currency_display(
            match_country,
            detail.target_value,
            source_country,
        )
        diff = target_income - source_income
        direction = t(language, "more") if diff > 0 else t(language, "less")
        title = t(language, "disposable_income")
        source_line = t(
            language,
            "in_place_roughly_currency",
            place=source_name,
            value=figure(f"{format_estimate(source_income)} {home_currency}"),
        )
        target_line = t(
            language,
            "in_place_roughly_currency",
            place=match_name,
            value=figure(f"{format_estimate(target_income)} {home_currency}"),
        )
        if abs(diff) < 1:
            diff_line = t(language, "almost_same")
        else:
            diff_line = t(
                language,
                "roughly_currency_more_less",
                value=figure(f"{format_estimate(abs(diff))} {home_currency}"),
                direction=direction,
            )

    elif detail.label == "Turnout":
        title = t(language, "people_voted_last_election")
        source_line = t(language, "turnout_line", place=source_name, value=figure(f"{round(detail.source_value):.0f}"))
        target_line = t(language, "turnout_line", place=match_name, value=figure(f"{round(detail.target_value):.0f}"))
        diff = detail.target_value - detail.source_value
        direction = t(language, "more") if diff > 0 else t(language, "less")
        if abs(diff) < 0.5:
            diff_line = t(language, "almost_same")
        else:
            diff_line = t(language, "turnout_diff", value=figure(f"{round(abs(diff)):.0f} out of 100"), direction=direction)

    elif detail.label == "Population density":
        title = t(language, "people_per_square_kilometre")
        population_detail = factor_lookup["Population"]
        source_area = population_detail.source_value / detail.source_value if detail.source_value else 0.0
        target_area = population_detail.target_value / detail.target_value if detail.target_value else 0.0
        source_line = t(language, "in_place_about", place=source_name, value=figure(f"{format_estimate(detail.source_value)} per km²"))
        target_line = t(language, "in_place_about", place=match_name, value=figure(f"{format_estimate(detail.target_value)} per km²"))
        diff = detail.target_value - detail.source_value
        direction = t(language, "more") if diff > 0 else t(language, "less")
        if abs(diff) < 1:
            diff_line = t(language, "almost_same")
        else:
            diff_line = t(language, "density_diff", value=figure(f"{format_estimate(abs(diff))} per km²"), direction=direction)
        note_line = t(
            language,
            "area_note",
            source_area=figure(f"{format_estimate(source_area)} km²"),
            source_name=source_name,
            target_area=figure(f"{format_estimate(target_area)} km²"),
            target_name=match_name,
        )

    elif detail.label == "Cars":
        title = t(language, "cars")
        population_detail = factor_lookup["Population"]
        source_cars = population_detail.source_value * detail.source_value / 1000.0
        target_cars = population_detail.target_value * detail.target_value / 1000.0
        source_line = t(language, "in_place_about", place=source_name, value=figure(format_estimate(source_cars)))
        target_line = t(language, "in_place_about", place=match_name, value=figure(format_estimate(target_cars)))
        diff = target_cars - source_cars
        direction = t(language, "more") if diff > 0 else t(language, "less")
        if abs(diff) < 1:
            diff_line = t(language, "almost_same")
        else:
            diff_line = t(language, "about_more_less", value=figure(format_estimate(abs(diff))), direction=direction)

    block_class = get_factor_block_class(detail.standardized_gap)
    note_html = ""
    if note_line:
        note_html = f'<div class="nabour-small">{note_line}</div>'
    st.markdown(
        f"""
        <div class="{block_class}">
          <div class="nabour-factor-value">{title}</div>
          <div class="nabour-compare-name">{source_line}</div>
          <div class="nabour-compare-name">{target_line}</div>
          <div class="nabour-compare-diff">{diff_line}</div>
          {note_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_statistics_box(match) -> None:
    language = get_language()
    rows = [
        f"| {t(language, 'factor_column')} | {t(language, 'gap_column')} |",
        "| --- | ---: |",
    ]
    for detail in match.factor_details:
        rows.append(
            f"| {factor_label(language, detail.label)} | {detail.standardized_gap:.2f} |"
        )
    st.markdown("\n".join(rows))


def render_explanations_box() -> None:
    language = get_language()
    info = get_info(language, get_selected_pair_id())
    lines = []
    for english_label, explanation in info["factors"].items():
        lines.append(
            f"<div class='nabour-small'><strong>{factor_label(language, english_label)}:</strong> {explanation}</div>"
        )
    lines.append(
        f"<div class='nabour-small'><strong>{t(language, 'income_note')}:</strong> {info['income_note']}</div>"
    )
    st.markdown("".join(lines), unsafe_allow_html=True)


def format_factor_list(labels: list[str], language: str) -> str:
    localized = [factor_label(language, label).lower() for label in labels]
    if not localized:
        return ""
    if len(localized) == 1:
        return localized[0]
    if len(localized) == 2:
        if language == "da":
            return f"{localized[0]} og {localized[1]}"
        if language == "sv":
            return f"{localized[0]} och {localized[1]}"
        return f"{localized[0]} and {localized[1]}"
    joiner = ", ".join(localized[:-1])
    last = localized[-1]
    if language == "da":
        return f"{joiner} og {last}"
    if language == "sv":
        return f"{joiner} och {last}"
    return f"{joiner}, and {last}"


def render_pair_step() -> None:
    language = get_language()
    st.markdown('<div class="nabour-topbar"><div class="nabour-topbar-title">Nabour</div></div>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="nabour-title">{t(language, "choose_pair_begin")}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="nabour-subtitle">{t(language, "choose_pair_subtitle")}</p>', unsafe_allow_html=True)

    for pair_spec in list_pair_specs():
        if st.button(
            f"{pair_label(language, pair_spec.pair_id)} · {pair_spec.reference_year}",
            key=f"pair-{pair_spec.pair_id}",
            disabled=not pair_spec.active,
        ):
            reset_after_pair_change(pair_spec.pair_id)
            st.rerun()
        if not pair_spec.active:
            st.markdown(
                f"<div class='nabour-small'>{t(language, 'pair_not_ready')} "
                f"({t(language, 'pair_reference_year', year=pair_spec.reference_year)})</div>",
                unsafe_allow_html=True,
            )


def render_country_step() -> None:
    language = get_language()
    pair_spec = get_pair_spec(get_selected_pair_id())
    st.markdown('<div class="nabour-topbar"><div class="nabour-topbar-title">Nabour</div></div>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="nabour-title">{pair_label(language, pair_spec.pair_id)}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="nabour-subtitle">{t(language, "choose_country_in_pair")}</p>', unsafe_allow_html=True)
    st.markdown(
        f"<div class='nabour-small'>{t(language, 'pair_reference_year', year=pair_spec.reference_year)}</div>",
        unsafe_allow_html=True,
    )
    st.write("")

    country_columns = st.columns(len(pair_spec.countries), gap="medium")
    for column, country_id in zip(country_columns, pair_spec.countries):
        with column:
            if st.button(country_cta_label(language, country_id), key=f"country-{country_id}"):
                reset_after_country_change(country_id)
                st.rerun()

    if st.button(t(language, "back"), key="back-to-pair"):
        st.session_state["current_step"] = "pair"
        st.session_state["source_country"] = None
        st.session_state["source_region"] = None
        st.session_state["source_municipality"] = None
        st.rerun()


def render_region_step(region_maps) -> None:
    language = get_language()
    country_id = st.session_state.get("source_country")
    country_name = country_label(language, country_id)
    regions = region_maps[country_id]
    region_names = sorted(regions)

    st.markdown('<div class="nabour-topbar"><div class="nabour-topbar-title">Nabour</div></div>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="nabour-title">{country_name}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="nabour-subtitle">{t(language, "choose_region_then_municipality")}</p>', unsafe_allow_html=True)

    if not region_names:
        st.markdown('<div class="nabour-small">No regions available for this pair/country yet.</div>', unsafe_allow_html=True)
        if st.button(t(language, "back"), key="back-to-country-empty"):
            st.session_state["current_step"] = "country"
            st.rerun()
        return

    selected_region = st.selectbox(
        t(language, "region"),
        options=region_names,
        index=0 if st.session_state.get("source_region") not in region_names else region_names.index(
            st.session_state["source_region"]
        ),
    )
    st.session_state["source_region"] = selected_region

    municipalities = regions.get(selected_region, [])
    if not municipalities:
        st.markdown('<div class="nabour-small">No municipalities available in this region yet.</div>', unsafe_allow_html=True)
        if st.button(t(language, "back"), key="back-to-country-empty-municipalities"):
            st.session_state["current_step"] = "country"
            st.rerun()
        return

    selected_municipality = st.selectbox(
        t(language, "municipality"),
        options=municipalities,
        index=0
        if st.session_state.get("source_municipality") not in municipalities
        else municipalities.index(st.session_state["source_municipality"]),
    )
    st.session_state["source_municipality"] = selected_municipality

    col1, col2 = st.columns([1, 2], gap="small")
    with col1:
        if st.button(t(language, "back"), key="back-to-country"):
            st.session_state["current_step"] = "country"
            st.rerun()
    with col2:
        if st.button(t(language, "find_matches"), key="find-matches"):
            st.session_state["current_step"] = "matches"
            st.rerun()


def render_matches_step(matcher_state) -> None:
    language = get_language()
    source_country = st.session_state["source_country"]
    source_municipality = st.session_state["source_municipality"]
    target_country = get_target_country_id(matcher_state.pair_spec, source_country)
    matches = compute_cross_border_matches(
        source_country_id=source_country,
        source_municipality=source_municipality,
        matcher_state=matcher_state,
        top_n=5,
    )

    st.markdown('<div class="nabour-topbar"><div class="nabour-topbar-title">Nabour</div></div>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="nabour-title">{t(language, "results_title", municipality=source_municipality)}</h1>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="nabour-meta">{t(language, "results_intro", country=country_label(language, target_country), municipality=source_municipality)}</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 2], gap="small")
    with col1:
        if st.button(t(language, "back"), key="back-to-region"):
            st.session_state["current_step"] = "region"
            st.rerun()
    with col2:
        if st.button(t(language, "start_over"), key="start-over"):
            st.session_state["current_step"] = "pair"
            st.session_state["pair_id"] = None
            st.session_state["source_country"] = None
            st.session_state["source_region"] = None
            st.session_state["source_municipality"] = None
            st.rerun()

    st.write("")
    for match in matches:
        st.markdown(
            f'<div class="nabour-matchbar"><div class="nabour-matchbar-title">{match.municipality}</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="nabour-small">{t(language, "result_closest", municipality=source_municipality, factors=format_factor_list(list(match.similar_factors), language))}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="nabour-small">{t(language, "result_gaps", factors=format_factor_list(list(match.different_factors), language))}</div>',
            unsafe_allow_html=True,
        )
        with st.expander(t(language, "compare_places")):
            factor_lookup = {item.label: item for item in match.factor_details}
            for detail in match.factor_details:
                render_factor_comparison_block(
                    source_name=source_municipality,
                    source_country=source_country,
                    match_name=match.municipality,
                    match_country=match.country_id,
                    detail=detail,
                    factor_lookup=factor_lookup,
                )
            with st.expander(t(language, "show_statistics")):
                render_statistics_box(match)
        st.write("")


def main() -> None:
    st.set_page_config(page_title="nabour", page_icon="n", layout="centered")
    apply_styles()

    if "current_step" not in st.session_state:
        st.session_state["current_step"] = "pair"
        st.session_state["pair_id"] = None
        st.session_state["source_country"] = None
        st.session_state["source_region"] = None
        st.session_state["source_municipality"] = None
    if "pair_id" not in st.session_state:
        st.session_state["pair_id"] = None
    if "language" not in st.session_state:
        st.session_state["language"] = DEFAULT_LANGUAGE

    top_left, top_right = st.columns([12, 1], gap="small")
    with top_right:
        render_settings_menu()

    if st.session_state["current_step"] == "pair" or not st.session_state.get("pair_id"):
        render_pair_step()
        return

    pair_id = st.session_state["pair_id"]
    pair_spec = get_pair_spec(pair_id)
    if not pair_spec.active:
        st.session_state["current_step"] = "pair"
        st.rerun()

    matcher_state = get_matcher_state(pair_id)
    region_maps = get_region_maps(pair_id)

    if st.session_state["current_step"] == "country" or not st.session_state.get("source_country"):
        render_country_step()
        return
    if st.session_state["current_step"] == "region" or not st.session_state.get("source_municipality"):
        render_region_step(region_maps)
        return
    render_matches_step(matcher_state)


if __name__ == "__main__":
    main()
