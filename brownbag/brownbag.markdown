Brownbag
========

*2013-05-13 NYU*

Probabilistic detection and analysis of transiting exoplanets using Kepler
--------------------------------------------------------------------------

**About Me**

* I've worked on lots of things:
  - Galaxy dynamics
  - Variable stars
  - Photometric self-calibration
  - Image modeling: fast and traditional
  - MCMC sampling techniques
  - now, exoplanets
* Underlying it all: data analysis (preferably probabilistic) and ambitious
  engineering projects
* Also involved and interested in the open source world

**emcee**

* My most successful project to date:
  - ~50 citations in the past 15 months
  - active community online
  - led to exciting collaborations and talk invitations
* Maybe a brief explanation of the algorithm and the interface because it is
  doubly relevant

**Why study exoplanets?**

*

**How do you study exoplanets?**

* Radial velocities, astrometry, direct detection, transits
* in fact most discoveries use a few of these techniques
* the most productive method recently has been transits using Kepler and
  that's what I'm going to talk about
* for transit searches, you just monitor the brightness of many stars as a
  function of time with fairly high cadence... sometimes you get lucky and a
  planet (or system) of planets will

**Kepler**

* I'm not at all an expert yet
* Some info about Kepler itself:
  - earth trailing, etc.
  - two types of cadences
  - science goals
* I'm not going to talk a lot about the many exciting discoveries that have
  been made so far except where they tie into what I'm working on but I'll
  list a few here:
  - how many candidates?
  - how many confirmed planets?
  - also stellar science.

**A funny way of writing down the Kepler data analysis**

* Remind everyone that this is only a sketch... don't interrupt too early or
  take it too seriously
* Sketch the graphical model, the generative procedure:
  - to start, there is some distribution of stars in the Universe---draw a
    star from that
  - there is also some distribution of planets in the Universe---draw a planet
    from that... but to be realistic, the planet parameters probably depend on
    which system it's in so add that edge... also there is sometimes more
    than one planet in the system---add the plate
  - then this system and all of these parameters can generate some
    observations (note that this "observation" node some huge heterogeneous
    object)
  - and then in practice, we have now observed many systems so add that plate
    too
  - there's something (big) missing: the systematics. This includes things
    like the selection function of the survey and a model of the variable
    background of the survey
* I like to argue that many of the Kepler science goals can be written down in
  this form

**My project**

* I've been working on a few components of this model and I'm going to talk
  about 2 today:
  - *Untrendy*: a horrifying hack for removing systematic trends in the data
  - *Bart*: an efficient and flexible inference engine for doing the required
    internal marginalizations

**Untrendy**

*Switch to slides*

* Start by demoing untrendy on Kepler-10
  - Kepler 10 is an older Sun-like main sequence star (Teff=5627, M=0.895,
    R=1.056)
* First you go and download the light curve data... the raw aperture
  photometry looks like shit...
* There is also a column that has been corrected for a lot of the shit... it's
  called Pre-search Data Conditioning (PDC)... still looks a bit like shit
* That's why we came up with our algorithm called untrendy... looks sick.
* I'm not being totally fair... no one would actually use the PDC data, right?
* Should at least use a median filter! This actually works really well!
* There's a new algorithm (Stumpe+ 2012 & Smith+ 2012) that will do a much
  better job by using statistics of nearby light curves
* Main features of untrendy:
  - flexible but constrained and tunable non-parametric model
  - robust outlier (transit) rejection using IRLS
  - automatic discontinuity detection e.g. Sudden Pixel Sensitivity Dropouts
    (SPSDs)
  - extremely fast, local and scalable---only marginally slower than the
    median model
  - might even be *more* useful than the MAP algorithm for transit searches
    and parameter estimation problems because it actually will remove stellar
    variability signals... clearly much worse for stellar studies
* How does it work?
  1. fit a cubic spline model with knots every few days to the light curve
     using IRLS
     - IRLS is awesome because it is an extremely robust and efficient method
     - similar to sigma clipping but the transition is smooth... it can
       probably described as some approximation of a proper mixture model
  2. Find discontinuities and add knots or just break dataset
  3. Return to set 1 and then iterate until no more discontinuities are found
* K, looks good. But, WTF have we done?! This is clearly a horrifying
  procedure to apply to your data!
* It has introduced all sort of correlated noise and it might have killed some
  of the transit signal
* This is an example of a case where you have to be really clear about what
  you want to *do* with the data:
  - for finding transits in the 300k light curves with >100k samples each, you
    want an extremely fast technique that is robust/automated and removes as
    much contaimination as possible
  - for studying stellar variability, you want an algorithm that only removes
    systematic effects ... obviously much more difficult so you have to be
    will to spend more cash
  - for estimating the parameters of a planetary system, either mode could
    work but if you keep the stellar variability componenet, you'll need a
    model of the variability within your procedure and I have a feeling that
    it'll probably look awefully similar to the one that we're using for
    untrending anyways... so maybe you should just remove it all
  - another option which the err-Bayesian (or whatever it is) inside of me
    prefers would be to forward model the whole thing: the parameters in your
    model include the knot values as well as the physical parameters and I
    have some ideas about how to do this efficiently but I'll come to that
    later.


**Bart**

* Bart is a parameter estimation part of the graphical model.
* The setup is as follows:
  - You have data (light curves [of different cadences], radial velocities,
    contraints from astrometry, stellar spectra, whatever)
  - you have parameterized prior functions on the population parameters
  - you want the distribution of planetary/stellar parameters that are
    consistent with the data
* p(model | data) --- MCMC!
* Following the rules of math: we can invert... need likelihood function.


**Mandel and Agol (2002)**

* Transit model == M&A 02 (almost 600 citations)
* Why is this so hard? Can solve Kepler, etc.
* Geometry of a transit...
* Fraction of occulted flux: lambda
* In the case of two overlapping uniform disks, this is pretty easy... just a
  geometric factor (I'm not really that smart so I looked up the answer on the
  internet but it's not hard to solve).
* What gets hard is that a star is *not* a uniformly illuminated disk:
  limb-darkening
* the shape of the light curve is *very* different and almost all of the
  information in the data comes from the detailed shape of the ingress and
  egress in the LC so you have to model it very precisely
* It's clear from our measurements of the Sun and the shapes of light curves
  that this effect is present and *important*
* M&A derived "analytic" expressions for the effects of limb darkening on the
  shape of the light curve for 2 different LD parameterizations (quadratic and
  quartic in cos theta) --- observations of the Sun and stellar atmosphere
  simulations say that this is a pretty reasonable form
* There are two main problems with this (not particularly serious but I need
  to come up with problems so that I have a job)
  1. we can really only measure the LDP of the Sun...
  2. the analytic form requires computing all sorts of special functions
     numerically which isn't actually particularly efficient... there might be
     smarter ways to do it but when I benchmark the method that I'm going to
     describe against the M&A code (both written in basic Fortran) my general
     model is just as efficient to compute!


**The Bart idea**

* Ridiculously dumbass but awesome.
* A little story: when I started working on this stuff, I tried to reproduce
  the M&A results and got pretty frustrated cause I tend to never trust other
  peoples' code. I wrote a test that checked the M&A method against a
  numerically integrated solution and quickly discovered that the numerical
  solution was just as fast! So that's what we decided to use
* The fraction of occulted flux is computed by the area integral...
* Computational complexity scales linearly with the number of bins with a
  small multiplier so you can easily have a fairly large number of bins with
  an arbitrary model
* I think that this is interesting for several reasons:
  1. the basic engineering point that sometimes it's reasonable to use the
     simplest idea
  2. it gives you an easy way of modeling and potentially discovering
     departures from the standard limb darkening model
  3. it might provide a way to *measure* the limb darkening profiles of stars
     using multiple planet systems
* So this exists: this part of Bart is a stand alone Fortran library that
  takes in a set of planetary and stellar parameters and returns a model light
  curve and radial velocities. It's pretty sweet.


**What else is Bart?**

* Bart isn't just this novel likelihood function... it also has a full suite
  of Python tools for working with the data.
* In particular, it has an expressive model building syntax and it interfaces
  directly with the standard Python optimization libraries and emcee (my MCMC
  sampler).
* I won't get into the details of everything that exists because it would be
  terribly boring but I do want to comment on the fact that I've been working
  a lot on documentation and testing so things are pretty robust and easy to
  use.


**Bart demo**







