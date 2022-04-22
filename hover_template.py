def pib_hover_template():
    return "<br>".join(
        [
            "<b>Mois: </b>%{x}",
            "<b>PIB: </b>%{y}$",
            "<extra></extra>",
        ]
    )


def inflation_hover_template():
    return "<br>".join(
        [
            "<b>Produit ou groupe de produits: </b>%{y}",
            "<b>Mois: </b></b>%{x}",
            "<b>Variation annuelle: </b>%{z}%",
            "<extra></extra>",
        ]
    )

def revenus_total_hover_template():
    return "<br>".join(
        [
            "<b>Trimestre: </b>%{x}",
            "<b>Revenus: </b>%{y}$",
            "<extra></extra>",
        ]
    )

def revenus_hover_template(percent):
    return "<br>".join(
        [
            "%{customdata[0]} <br>",
            "<b>Trimestre: </b>%{x}",
            "<b>Revenus: </b>%{y}" + ("%" if percent else "$"),
            "<extra></extra>",
        ]
    )


def depenses_hover_template():
    return "<br>".join(
        [
            "%{text} <br>",
            "<b>Trimestre: </b>%{x}",
            "<b>Dépenses: </b>%{y}$",
            "<extra></extra>",
        ]
    )


def caracteristiques_hover_template(type):
    return "<br>".join(
        [
            "<b>Mois: </b>%{x}",
            "<b>" + type + ": </b> %{y:.1f}%",
            "<extra></extra>",
        ]
    )


def horaires_hover_template():
    return "<br>".join(
        [
            "%{customdata[0]} <br>",
            "<b>Salaire: </b> %{x:.1f}$",
            "<b>Industrie: </b> %{y}" "<extra></extra>",
        ]
    )


def salaires_salairemoy_hover_template():
    return "<br>".join(
        [
            "<b>Année: </b>%{x}",
            "<b>Salaire: </b>%{y:.2f}$",
            "<extra></extra>",
        ]
    )

def salaires_bar_hover_template():
    return "<br>".join(
        [
            "<b>Industrie: </b>%{y}",
            "<b>Salaire: </b>%{x:.2f}$",
            "<extra></extra>",
        ]
    )


def paralleles_hover_template():
    return "<br>".join(
        [
            "<b>Industrie: </b>%{y}",
            "<b>Salaire: </b>%{x:.2f}$",
            "<extra></extra>",
        ]
    )
