#Portfolio Commons Wrap Up

The [Portfolio Commons project](/projects/portfolio-commons) aimed to make it possible to deposit content from the [Mahara ePortfolio](https://mahara.org/) platform into a remote learning repository, using the [SWORDv2](http://swordapp.org) protocol. This would make it easier to commit Open Educational Resources to repositories, by allowing users to deposit their content from within the eLearning tools they are already using.

The project was led by the [University of the Arts London](http://www.arts.ac.uk/) (UAL) in the [Centre for Learning & Teaching in Art & Design (CLTAD)](http://www.arts.ac.uk/cltad/), and funded by [Jisc](http://www.jisc.ac.uk).  Cottage Labs became involved in a minor supporting role to help with the design and implementation of the SWORDv2 portion of the project.  Without much experience in the creative arts sector or the eLearning space, we were glad to get involved to learn more, while helping with the technical details.

Our involvement in the project focussed on a couple of areas: understanding the needs of the project from a deposit point of view, providing a technical design, and then assisting in minor technical details to do with the deposit protocol.  Meanwhile UAL built all of the technology at the Mahara end and liaised with the service providers [Jorum](http://www.jorum.ac.uk) and [EPrints](http://eprints.org) so that we could effect a deposit from the eLearning system.

The rest of this post describes the work that we carried out here at Cottage Labs, but you should check out [the project blog](http://portfoliocommons.myblog.arts.ac.uk/) for all the other great content.

##Requirements Analysis

Mahara is a large and sophisticated system that supports students in managing their electronic portfolios, so integrating a deposit solution was not going to be straightforward.  We carried out a requirements gathering process with our UAL colleagues to figure out where in the student workflows we were likely to want deposit options, and what would be deposited at that stage.  We pulled out quite a few requirements, which we won't enumerate here, but they included things like:

* Mahara should be able to deliver a packaged OER to a repository, formed of either a single Page or a Collection of multiple Pages.

* The deposit process should create a single repository object per Mahara Page when a Page is deposited, or a single repository object per Mahara Collection when a Collection is deposited

* The user should be able to easily tell when a page they are looking at has been deposited into the repository

* Only publicly accessible pages should be exportable to the repository.

* It is important to preserve the long-term existence of the OER resource.  The formatting of the resource is important, but not as important as the content itself.

With these requirements we know more about how we want to package the content, where in Mahara deposit operations should be enabled, we can therefore infer the SWORDv2 protocol operations that we need to employ.

##Technical Design

Knowing the requirements for deposit, we could go on and propose specific [technical design](https://docs.google.com/document/d/1d25v5xvTp9nJIlmP4ydo9M9y9oMxWDzt6NV7JJYFNHo/edit?usp=sharing) decisions.  For example, for the user interface we could say the following:

* We want a page presenting deposit options for all pages and collections
* We also want deposit options available on Page and Collection management pages
* The user should be given an option to select the deposit endpoint (i.e. which repository to deposit into)

We also originally recommended to use the [Leap2A](http://www.leapspecs.org/2A/) package format that comes as standard with Mahara, but over the course of the project UAL found that this was not so convenient and instead chose to go with [METS](http://www.loc.gov/standards/mets/) instead.  As it turned out this was going to fit well with SWORDv2 and impact on what we did for our technical contribution to the project later on.

We also provided interaction diagrams for the SWORDv2 interactions, some examples of which are below:

<div class="row-fluid" style="margin-bottom: 15px;">
    <div class="span6 well">
        <h3>Initial deposit</h3>
         <img src="/media/pc_initial_deposit.png" class="img span12">
    </div>
    
    <div class="span6 well">
        <h3>Get information on repository item</h3>
        <img src="/media/pc_lookup_item.png" class="img span12">
    </div>
</div>

##SWORDv2 and METS support

Most of the technical development was carried out by UAL and also Mimas for the Jorum parts later in the project.  We found that our best contribution was to offer some enhancements to the standard DSpace SWORDv2 implementation that Jorum would utilise, so that it would support METS natively.  We therefore extended an existing enhanced version of DSpaceSWORDv2 that we had been working on for the [DUO project](/projects/duo), released it as a [separate module](https://github.com/swordapp/DSpaceSWORDv2) in the [sword github account](https://github.com/swordapp) and implemented METS support for both create and update operations.  Previously METS support was dropped in DSpace from SWORDv1 to SWORDv2, due to complexities with the package plugins, but we were able to use the Portfolio Commons project to spend some time addressing that.  These changes will ultimately become part of the main DSpace release, and are already in use in Jorum.

##Final Remarks

Being part of this project was really valuable for us in understanding several new spaces: the creative arts and eLearning.  We were also glad to find another tie up with Jorum (with whom we worked on the [Jorum Paradata project](/projects/jorum-paradata)).  The software outputs that we produced from this project will be useful to other SWORDv2 users in the future.  So for a short project (from our point of view) there was a lot here.  We're looking forward to seeing the final outputs of the project, as UAL drive it to its successful conclusion over the next few months.











Original Title: Portfolio Commons Wrap Up
Original Author: richard
Tags: mahara, portfoliocommons, richard, ual, jorum, mimas, news, dspace, swordv2
Created: 2013-03-01 2217
Last Modified: 2013-09-22 1645
