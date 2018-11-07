# G4HE Futures

As the G4HE project draws to a close this post reflects on the key issues that we have encountered which need to be addressed for the tools developed to become a service which can be sustained.

There are three key areas which users and testers of the tools identified as being need of enhancement

* **Not full coverage of all funding** - at the moment the tools rely entirely on the Gateway to Research data available via its API.  This provides coverage of the 7 research councils (RCUK) and the Technology Strategy Board (TSB).  Anecdotally, this accounts for between 30% and 50% of an average research institution's grant income, meaning that while the data is useful it does not provide the research managers and planning departments with a complete picture of grant income and collaborations.

* **Not yet suitable for systematic reports** - due to some simplifications or limitations in the data, the tools are not yet quite ready to be used to produce the systematic kinds of reports that research managers/planning departments prepare for senior management.  A key example is in the break-down of funding: G4HE deals with grant funding at a project level, and does not have the break-down of that funding across the project partners, or a clear knowledge of where funding was distributed; this means that an institution's total grant income from a project - and therefore in aggregate - cannot be accurately calculated.

* **Data quality requires work** - there are two areas where data quality has been an issue:
    * name disambiguation - there is huge variation in the use of institutional names, meaning that it is not possible to be sure that you are looking at all the grants for a given institution.  For example, the "University of Edinburgh" may also be named "Edinburgh University", and an equivalence between these organisations is not always clear.
    * publications data - publications data has not been a focus of GtR and it is known that the number of publications registered against grants is incomplete.  This means reports based on publications cannot be relied upon at this stage.

We have been aware of these problems throughout the project, thanks to the user testing we received from the ARMA group, and have been developing longer term plans to deal with them.  Outlined below are our main angles of attack.

## Find other data sources

We already evaluated the Grist API for use with G4HE; this provides funding data about Europe PMC projects.  At the time of evaluation, the Grist API did not provide sufficient data to incorporate into our reports, but the project is drafting a proposal to the maintainers to extend the data to make it more suitable.

It would also be useful for us to find other sources of fuding data - in particuler EU data - so that we could increase our coverage on an average research institution's grant income.

## Data Cleanup

A lot of the data in Gateway to Research, and thus G4HE, has been human-entered into the systems which captured the information originally.  This has introduced a lot of errors such as mis-spellings and inconsistent use of terms (in particular institution names).  The ideal situation would be for those problems to be fixed at-source (e.g. through the use of controlled vocabularies), but in the mean time, the project has been carrying out some text analysis to see if it is possible to de-duplicate institution names, which would give us a big leg-up.

As part of an investigation into this, we have developed some basic crowd-sourcing tools to allow users of the data to assert to us when organisations are similar.

## Direct upload from CRIS

The canonical source of a lot of the information that institutions want to perform reports over actually comes from the institutions themselves.  Therefore there is value in exploring the possibility that institutions might provide the tools with the missing or incorrect data.  One obvious case is to address the limited quality of the GtR publications data - if institutions could provide the system with definitive lists of their publications, then the dataset could become significantly enhanced, and reports around publications would become much more reliable.

During the project, team members met with the big three CRIS vendors: Atira (Pure), Converis (Avedas), Symplectic (Elements), to discuss their interest in the tools and the possibility of integration.  There was general agreement that the tools fitted a niche, and that the CRIS systems would be able to provide at least some of the data which the tools are missing.  Experiments to integrate institutional data with the tools are now planned.

## Direct from Funders

It would be valuable for UK institutions for us to increase the coverage of the tools for UK funders.  While we have the 7 RCUK funders and the TSB, a direct feed from the Wellcome Trust, for example, would be hugely beneficial.  There is a long-tail of UK funders, as well as funding to institutions which comes from private enterprise (e.g. Brunel University receives significant funding from Jaguar-Land Rover), and gathering information from all of them will be impossible.  Nonetheless an effort to engage the largest funders (such as Wellcome) and any umbrella organisations (such as the Association for Medical Research Charities (AMRC)) may prove worthwhile.



Original Title: G4HE Future
Original Author: richard
Tags: g4he, richard, news, rcuk, gtr, sustainability, grist
Created: 2014-04-14 1041
Last Modified: 2014-04-14 1600
