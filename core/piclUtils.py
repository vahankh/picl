# -*- coding: utf-8 -*-

def plural(word):
    """
    Converts a word to its plural form.
    """
    if word in IRREGULAR_NOUNS:
        # foot->feet, person->people, etc
        return IRREGULAR_NOUNS[word]
    elif word.endswith('fe'):
        # wolf -> wolves
        return word[:-2] + 'ves'
    elif word.endswith('f'):
        # knife -> knives
        return word[:-1] + 'ves'
    elif word.endswith('o'):
        # potato -> potatoes
        return word + 'es'
    elif word.endswith('us'):
        # cactus -> cacti
        return word[:-2] + 'i'
    elif word.endswith('on'):
        # criterion -> criteria
        return word[:-2] + 'a'
    elif word.endswith('y'):
        # community -> communities
        return word[:-1] + 'ies'
    elif word[-1] in 'sx' or word[-2:] in ['sh', 'ch']:
        return word + 'es'
    elif word.endswith('an'):
        return word[:-2] + 'en'
    else:
        return word + 's'


IRREGULAR_NOUNS = {
    "addendum": "addenda",
    "aircraft": "aircraft",
    "alga": "algae",
    "alumna": "alumnae",
    "alumnus": "alumni",
    "amoeba": "amoebae",
    "analysis": "analyses",
    "antenna": "antennae",
    "antithesis": "antitheses",
    "apex": "apices",
    "appendix": "appendices",
    "automaton": "automata",
    "axis": "axes",
    "bacillus": "bacilli",
    "bacterium": "bacteria",
    "barracks": "barracks",
    "basis": "bases",
    "beau": "beaux",
    "bison": "bison",
    "buffalo": "buffalo",
    "bureau": "bureaus",
    "cactus": "cacti",
    "calf": "calves",
    "carp": "carp",
    "census": "censuses",
    "chassis": "chassis",
    "cherub": "cherubim",
    "child": "children",
    "château": "châteaus",
    "cod": "cod",
    "codex": "codices",
    "concerto": "concerti",
    "corpus": "corpora",
    "crisis": "crises",
    "criterion": "criteria",
    "curriculum": "curricula",
    "datum": "data",
    "deer": "deer",
    "diagnosis": "diagnoses",
    "die": "dice",
    "dwarf": "dwarfs",
    "echo": "echoes",
    "elf": "elves",
    "elk": "elk",
    "ellipsis": "ellipses",
    "embargo": "embargoes",
    "emphasis": "emphases",
    "erratum": "errata",
    "faux pas": "faux pas",
    "fez": "fezes",
    "firmware": "firmware",
    "fish": "fish",
    "focus": "foci",
    "foot": "feet",
    "formula": "formulae",
    "fungus": "fungi",
    "gallows": "gallows",
    "genus": "genera",
    "goose": "geese",
    "graffito": "graffiti",
    "grouse": "grouse",
    "half": "halves",
    "hero": "heroes",
    "hoof": "hooves",
    "hovercraft": "hovercraft",
    "hypothesis": "hypotheses",
    "index": "indices",
    "kakapo": "kakapo",
    "knife": "knives",
    "larva": "larvae",
    "leaf": "leaves",
    "libretto": "libretti",
    "life": "lives",
    "loaf": "loaves",
    "locus": "loci",
    "louse": "lice",
    "man": "men",
    "matrix": "matrices",
    "means": "means",
    "medium": "media",
    "memorandum": "memoranda",
    "millennium": "millennia",
    "minutia": "minutiae",
    "moose": "moose",
    "mouse": "mice",
    "nebula": "nebulae",
    "nemesis": "nemeses",
    "neurosis": "neuroses",
    "news": "news",
    "nucleus": "nuclei",
    "oasis": "oases",
    "offspring": "offspring",
    "opus": "opera",
    "ovum": "ova",
    "ox": "oxen",
    "paralysis": "paralyses",
    "parenthesis": "parentheses",
    "person": "people",
    "phenomenon": "phenomena",
    "phylum": "phyla",
    "pike": "pike",
    "polyhedron": "polyhedra",
    "potato": "potatoes",
    "prognosis": "prognoses",
    "quiz": "quizzes",
    "radius": "radii",
    "referendum": "referenda",
    "salmon": "salmon",
    "scarf": "scarves",
    "self": "selves",
    "series": "series",
    "sheep": "sheep",
    "shelf": "shelves",
    "shrimp": "shrimp",
    "spacecraft": "spacecraft",
    "species": "species",
    "spectrum": "spectra",
    "squid": "squid",
    "stimulus": "stimuli",
    "stratum": "strata",
    "swine": "swine",
    "syllabus": "syllabi",
    "symposium": "symposia",
    "synopsis": "synopses",
    "synthesis": "syntheses",
    "tableau": "tableaus",
    "that": "those",
    "thesis": "theses",
    "thief": "thieves",
    "tomato": "tomatoes",
    "tooth": "teeth",
    "trout": "trout",
    "tuna": "tuna",
    "vertebra": "vertebrae",
    "vertex": "vertices",
    "veto": "vetoes",
    "vita": "vitae",
    "vortex": "vortices",
    "watercraft": "watercraft",
    "wharf": "wharves",
    "wife": "wives",
    "wolf": "wolves",
    "woman": "women"
}