from __future__ import annotations


INFO_CONTENT = {
    "en": {
        "about": [
            "`nabour` is a small Hedegreen Research tool.",
            "[Hedegreen Research](https://hedegreenresearch.com/)",
            "It tries to find the municipality in the other country that looks most like yours.",
            "It does not try to tell you where you should live.",
        ],
        "method": [
            "The tool uses the lowest common set of public numbers that Denmark and Sweden actually share.",
            "It compares municipalities on population, age 65+, education, income, turnout, population density, and cars.",
            "The matching motor works on normalized values so very different kinds of numbers can still be compared fairly.",
            "The front of the tool is simpler than the motor. Some values are translated into more human language in the UI.",
        ],
        "factors": {
            "Population": "Number of residents in the municipality.",
            "Age 65+": "Share of residents aged 65 or older.",
            "Education": "Share of residents with higher education.",
            "Income": "Country-local disposable income measure. Denmark and Sweden do not use the same raw unit here.",
            "Turnout": "Votes cast as a share of eligible voters.",
            "Population density": "Residents per square kilometre.",
            "Cars": "Passenger cars per 1,000 residents.",
        },
        "income_note": "The raw Denmark and Sweden income values do not start on one shared currency scale. The matcher harmonizes them internally, while the public display stays explicit about conversion and unit limits.",
    },
    "da": {
        "about": [
            "`nabour` er et lille værktøj fra Hedegreen Research.",
            "[Hedegreen Research](https://hedegreenresearch.com/)",
            "Det prøver at finde den kommune i det andet land der ligner din mest.",
            "Det prøver ikke at fortælle dig hvor du bør bo.",
        ],
        "method": [
            "Værktøjet bruger den laveste fælles mængde offentlige tal som Danmark og Sverige faktisk deler.",
            "Det sammenligner kommuner på befolkning, 65+, uddannelse, indkomst, valgdeltagelse, befolkningstæthed og biler.",
            "Selve motoren arbejder med normaliserede værdier, så meget forskellige slags tal stadig kan sammenlignes ordentligt.",
            "Forsiden er enklere end motoren. Nogle værdier bliver oversat til mere menneskeligt sprog i UI'et.",
        ],
        "factors": {
            "Population": "Antal indbyggere i kommunen.",
            "Age 65+": "Andel af indbyggerne der er 65 år eller ældre.",
            "Education": "Andel af indbyggerne med videregående uddannelse.",
            "Income": "Landelokalt mål for disponibel indkomst. Danmark og Sverige bruger ikke samme rå enhed her.",
            "Turnout": "Afgivne stemmer som andel af de stemmeberettigede.",
            "Population density": "Indbyggere per kvadratkilometer.",
            "Cars": "Personbiler per 1.000 indbyggere.",
        },
        "income_note": "De rå indkomsttal fra Danmark og Sverige starter ikke på én fælles pengeskala. Matcheren harmoniserer dem internt, mens den synlige visning er tydelig om omregning og begrænsninger.",
    },
    "sv": {
        "about": [
            "`nabour` är ett litet verktyg från Hedegreen Research.",
            "[Hedegreen Research](https://hedegreenresearch.com/)",
            "Det försöker hitta kommunen i det andra landet som liknar din mest.",
            "Det försöker inte tala om för dig var du borde bo.",
        ],
        "method": [
            "Verktyget använder den minsta gemensamma mängden offentliga siffror som Danmark och Sverige faktiskt delar.",
            "Det jämför kommuner på befolkning, 65+, utbildning, inkomst, valdeltagande, befolkningstäthet och bilar.",
            "Själva motorn arbetar med normaliserade värden så att olika slags siffror ändå kan jämföras rättvist.",
            "Framsidan är enklare än motorn. Vissa värden översätts till mer mänskligt språk i gränssnittet.",
        ],
        "factors": {
            "Population": "Antal invånare i kommunen.",
            "Age 65+": "Andel av invånarna som är 65 år eller äldre.",
            "Education": "Andel av invånarna med högre utbildning.",
            "Income": "Landsspecifikt mått på disponibel inkomst. Danmark och Sverige använder inte samma råa enhet här.",
            "Turnout": "Avgivna röster som andel av de röstberättigade.",
            "Population density": "Invånare per kvadratkilometer.",
            "Cars": "Personbilar per 1 000 invånare.",
        },
        "income_note": "De råa inkomstvärdena från Danmark och Sverige börjar inte på en gemensam valutaskala. Matcharen harmoniserar dem internt, medan den synliga visningen är tydlig med omräkning och begränsningar.",
    },
}


def get_info(language: str) -> dict[str, object]:
    return INFO_CONTENT.get(language, INFO_CONTENT["en"])
