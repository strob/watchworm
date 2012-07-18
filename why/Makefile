RECORDINGS = $(wildcard data/*.avi)

COMPOSITES = $(patsubst %,%.comp.png,$(RECORDINGS))
data/%.avi.comp.png: generate_composite.py data/%.avi
	python $^ $@

WEBMS = $(patsubst %,%.webm,$(RECORDINGS))
data/%.avi.webm: webm.py data/%.avi
	python $^ $@

FIRSTFRAMES = $(patsubst %,%.first.png,$(RECORDINGS))
data/%.avi.first.png: first_frame.py data/%.avi 
	python $^ $@

CONTOUR45 = $(patsubst %,%.contoursADP45.pkl,$(RECORDINGS))
CONTOUR45P = $(patsubst %,%.contoursADP45.png,$(RECORDINGS))
data/%.avi.contoursADP45.pkl: contours45.py data/%.avi
	python $^ $@

PATHS45 = $(patsubst %,%.pathADP45.pkl,$(RECORDINGS))
data/%.avi.pathADP45.pkl: paths.py data/%.avi.contoursADP45.pkl
	python $^ $@

CONTOUR60 = $(patsubst %,%.contoursMOT60.pkl,$(RECORDINGS))
CONTOUR60P = $(patsubst %,%.contoursMOT60.png,$(RECORDINGS))
data/%.avi.contoursMOT60.pkl: contours60.py data/%.avi data/%.avi.comp.png
	python $^ $@

PATHS60 = $(patsubst %,%.pathMOT60.pkl,$(RECORDINGS))
PATHS60P = $(patsubst %,%.pathMOT60.png,$(RECORDINGS))
data/%.avi.pathMOT60.pkl: paths.py data/%.avi.contoursMOT60.pkl data/%.avi.contoursMOT60.png
	python $^ $@

JSONS = Recording.json
$(JSONS) : $(RECORDINGS) jsonification.py
	python jsonification.py

GEN = $(COMPOSITES) $(CONTOUR45) $(CONTOUR45P) $(CONTOUR60) $(CONTOUR60P) \
      $(JSONS) $(FIRSTFRAMES) $(WEBMS) $(PATHS45) $(PATHS60) $(PATHS60P)

.PHONY : clean
clean : 
	rm $(GEN)

.PHONY : all
all : $(GEN)

