from __future__ import annotations

from data_loader import FACTOR_LABELS
from pair_registry import get_pair_spec


ABOUT_LINES = {
    "en": [
        "`nabour` is a small Hedegreen Research tool.",
        "[Hedegreen Research](https://hedegreenresearch.com/)",
        "It tries to find the municipality in the other country that looks most like yours.",
        "It does not try to tell you where you should live.",
    ],
    "da": [
        "`nabour` er et lille værktøj fra Hedegreen Research.",
        "[Hedegreen Research](https://hedegreenresearch.com/)",
        "Det prøver at finde den kommune i det andet land der ligner din mest.",
        "Det prøver ikke at fortælle dig hvor du bør bo.",
    ],
    "sv": [
        "`nabour` är ett litet verktyg från Hedegreen Research.",
        "[Hedegreen Research](https://hedegreenresearch.com/)",
        "Det försöker hitta kommunen i det andra landet som liknar din mest.",
        "Det försöker inte tala om för dig var du borde bo.",
    ],
    "no": [
        "`nabour` er et lite verktøy fra Hedegreen Research.",
        "[Hedegreen Research](https://hedegreenresearch.com/)",
        "Det prøver å finne kommunen i det andre landet som ligner mest på din.",
        "Det prøver ikke å fortelle deg hvor du bør bo.",
    ],
}

PAIR_METHOD_LINES = {
    "en": {
        "dk_se_v1": [
            "The tool uses the lowest common set of public numbers that Denmark and Sweden actually share.",
            "It compares municipalities on population, age 65+, education, income, turnout, population density, and cars.",
            "The matching motor works on normalized values so very different kinds of numbers can still be compared fairly.",
            "The front of the tool is simpler than the motor. Some values are translated into more human language in the UI.",
        ],
        "dk_no_2024_beta": [
            "The Denmark-Norway pair runs on a narrower 2024 beta layer: population, income, and population density.",
            "Denmark population and density are rebuilt for 2024 from official municipal population rows so the pair can share one real year.",
            "Age 65+, education, turnout, and cars stay out because the current Denmark-Norway overlap is not honest enough there yet.",
        ],
        "se_no_2024_beta": [
            "The Sweden-Norway pair runs on a 2024 structural layer with population, age 65+, education, income, and population density.",
            "Income is temporarily the latest Sweden municipal row (2023) while the rest of the pair stays on 2024.",
            "This is a live beta pair and the income-year mismatch is explicit.",
        ],
    },
    "da": {
        "dk_se_v1": [
            "Værktøjet bruger den laveste fælles mængde offentlige tal som Danmark og Sverige faktisk deler.",
            "Det sammenligner kommuner på befolkning, 65+, uddannelse, indkomst, valgdeltagelse, befolkningstæthed og biler.",
            "Selve motoren arbejder med normaliserede værdier, så meget forskellige slags tal stadig kan sammenlignes ordentligt.",
            "Forsiden er enklere end motoren. Nogle værdier bliver oversat til mere menneskeligt sprog i UI'et.",
        ],
        "dk_no_2024_beta": [
            "Danmark-Norge-paret kører på et smallere 2024 beta-lag: befolkning, indkomst og befolkningstæthed.",
            "Danmarks befolkning og tæthed er genopbygget til 2024 fra officielle kommunale befolkningstal, så parret faktisk kan dele ét rigtigt år.",
            "65+, uddannelse, valgdeltagelse og biler er stadig ude, fordi overlapet mellem Danmark og Norge ikke er ærligt nok der endnu.",
        ],
        "se_no_2024_beta": [
            "Sverige-Norge-paret kører på et 2024 strukturlag med befolkning, 65+, uddannelse, indkomst og befolkningstæthed.",
            "Indkomst er midlertidigt seneste svenske kommunerække (2023), mens resten af parret ligger på 2024.",
            "Dette er et live beta-par, og indkomst-års-forskellen er gjort tydelig.",
        ],
    },
    "sv": {
        "dk_se_v1": [
            "Verktyget använder den minsta gemensamma mängden offentliga siffror som Danmark och Sverige faktiskt delar.",
            "Det jämför kommuner på befolkning, 65+, utbildning, inkomst, valdeltagande, befolkningstäthet och bilar.",
            "Själva motorn arbetar med normaliserade värden så att olika slags siffror ändå kan jämföras rättvist.",
            "Framsidan är enklare än motorn. Vissa värden översätts till mer mänskligt språk i gränssnittet.",
        ],
        "dk_no_2024_beta": [
            "Danmark-Norge-paret kör på ett smalare 2024 beta-lager: befolkning, inkomst och befolkningstäthet.",
            "Danmarks befolkning och täthet är återbyggda till 2024 från officiella kommunrader så att paret faktiskt kan dela ett riktigt år.",
            "65+, utbildning, valdeltagande och bilar är fortfarande ute eftersom överlappet mellan Danmark och Norge ännu inte är ärligt nog där.",
        ],
        "se_no_2024_beta": [
            "Sverige-Norge-paret kör på ett 2024-strukturlager med befolkning, 65+, utbildning, inkomst och befolkningstäthet.",
            "Inkomst är tillfälligt senaste svenska kommunrad (2023), medan resten av paret ligger på 2024.",
            "Detta är ett live betapar och inkomst-årsskillnaden är explicit.",
        ],
    },
    "no": {
        "dk_se_v1": [
            "Verktøyet bruker den laveste felles mengden offentlige tall som Danmark og Sverige faktisk deler.",
            "Det sammenligner kommuner på befolkning, 65+, utdanning, inntekt, valgdeltakelse, befolkningstetthet og biler.",
            "Selve motoren arbeider med normaliserte verdier, slik at veldig ulike typer tall likevel kan sammenlignes på en rettferdig måte.",
            "Forsiden er enklere enn motoren. Noen verdier blir oversatt til mer menneskelig språk i grensesnittet.",
        ],
        "dk_no_2024_beta": [
            "Danmark-Norge-paret kjører på et smalere 2024 beta-lag: befolkning, inntekt og befolkningstetthet.",
            "Danmarks befolkning og tetthet er bygget opp igjen for 2024 fra offisielle kommunerader, slik at paret faktisk kan dele ett reelt år.",
            "65+, utdanning, valgdeltakelse og biler er fortsatt ute fordi overlapet mellom Danmark og Norge ennå ikke er ærlig nok der.",
        ],
        "se_no_2024_beta": [
            "Sverige-Norge-paret kjører på et 2024-strukturlag med befolkning, 65+, utdanning, inntekt og befolkningstetthet.",
            "Inntekt er midlertidig siste svenske kommunerad (2023), mens resten av paret holder 2024.",
            "Dette er et live betapar, og årsforskjellen på inntekt er eksplisitt.",
        ],
    },
}

FACTOR_EXPLANATIONS = {
    "en": {
        "Population": "Number of residents in the municipality.",
        "Age 65+": "Share of residents aged 65 or older.",
        "Education": "Share of residents with higher education.",
        "Income": "Country-local disposable income measure. Denmark, Sweden, and Norway do not use the same raw unit here.",
        "Turnout": "Votes cast as a share of eligible voters.",
        "Population density": "Residents per square kilometre.",
        "Cars": "Passenger cars per 1,000 residents.",
    },
    "da": {
        "Population": "Antal indbyggere i kommunen.",
        "Age 65+": "Andel af indbyggerne der er 65 år eller ældre.",
        "Education": "Andel af indbyggerne med videregående uddannelse.",
        "Income": "Landelokalt mål for disponibel indkomst. Danmark, Sverige og Norge bruger ikke samme rå enhed her.",
        "Turnout": "Afgivne stemmer som andel af de stemmeberettigede.",
        "Population density": "Indbyggere per kvadratkilometer.",
        "Cars": "Personbiler per 1.000 indbyggere.",
    },
    "sv": {
        "Population": "Antal invånare i kommunen.",
        "Age 65+": "Andel av invånarna som är 65 år eller äldre.",
        "Education": "Andel av invånarna med högre utbildning.",
        "Income": "Landsspecifikt mått på disponibel inkomst. Danmark, Sverige och Norge använder inte samma råa enhet här.",
        "Turnout": "Avgivna röster som andel av de röstberättigade.",
        "Population density": "Invånare per kvadratkilometer.",
        "Cars": "Personbilar per 1 000 invånare.",
    },
    "no": {
        "Population": "Antall innbyggere i kommunen.",
        "Age 65+": "Andel av innbyggerne som er 65 år eller eldre.",
        "Education": "Andel av innbyggerne med høyere utdanning.",
        "Income": "Landlokalt mål på disponibel inntekt. Danmark, Sverige og Norge bruker ikke samme rå enhet her.",
        "Turnout": "Avgitte stemmer som andel av de stemmeberettigede.",
        "Population density": "Innbyggere per kvadratkilometer.",
        "Cars": "Personbiler per 1 000 innbyggere.",
    },
}

INCOME_NOTES = {
    "en": "The raw income values do not start on one shared currency scale. The matcher harmonizes them internally pair by pair, while the public display stays explicit about conversion and unit limits.",
    "da": "De rå indkomsttal starter ikke på én fælles pengeskala. Matcheren harmoniserer dem internt pair for pair, mens den synlige visning er tydelig om omregning og begrænsninger.",
    "sv": "De råa inkomstvärdena börjar inte på en gemensam valutaskala. Matcharen harmoniserar dem internt pair för pair, medan den synliga visningen är tydlig med omräkning och begränsningar.",
    "no": "De rå inntektstallene starter ikke på én felles pengeskala. Matcheren harmoniserer dem internt pair for pair, mens den synlige visningen er tydelig om omregning og begrensninger.",
}


def get_info(language: str, pair_id: str) -> dict[str, object]:
    active_language = language if language in ABOUT_LINES else "en"
    pair_spec = get_pair_spec(pair_id)
    factor_labels = [FACTOR_LABELS[key] for key in pair_spec.factor_keys]
    return {
        "about": ABOUT_LINES[active_language],
        "method": PAIR_METHOD_LINES[active_language][pair_spec.method_note_key],
        "factors": {
            label: FACTOR_EXPLANATIONS[active_language][label]
            for label in factor_labels
        },
        "income_note": INCOME_NOTES[active_language],
    }
