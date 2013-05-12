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

**Kepler**

* I'm not at all an expert yet
* Some info about Kepler itself:
  - specs
  - science goals
* I'm not going to talk a lot about the many exciting discoveries that have
  been made so far except where they tie into what I'm working on but I'll
  list a few here:
  - blah

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

