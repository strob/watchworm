RECORDINGS = $(wildcard data/*.avi)

COMPOSITES = $(patsubst %,%.comp.png,$(RECORDINGS))
data/%.avi.comp.png: generate_composite.py data/%.avi
	python $^ $@

FIRSTFRAMES = $(patsubst %,%.first.png,$(RECORDINGS))
data/%.avi.first.png: first_frame.py data/%.avi 
	python $^ $@

CONTOUR45 = $(patsubst %,%.contoursADP45.pkl,$(RECORDINGS))
CONTOUR45P = $(patsubst %,%.contoursADP45.png,$(RECORDINGS))
data/%.avi.contoursADP45.pkl: contours45.py data/%.avi
	python $^ $@

CONTOUR60 = $(patsubst %,%.contoursMOT60.pkl,$(RECORDINGS))
CONTOUR60P = $(patsubst %,%.contoursMOT60.png,$(RECORDINGS))
data/%.avi.contoursMOT60.pkl: contours60.py data/%.avi data/%.comp.png
	python $^ $@


JSONS = Recording.json
$(JSONS) : $(RECORDINGS) jsonification.py
	python jsonification.py

GEN = $(COMPOSITES) $(CONTOUR45) $(CONTOUR45P) $(CONTOUR60) $(CONTOUR60P) \
      $(JSONS) $(FIRSTFRAMES)

.PHONY : clean
clean : 
	rm $(GEN)

.PHONY : all
all : $(GEN)

