RECORDINGS = $(wildcard data/*.avi)

# XXX: account for both inputs?
COMPOSITES = $(patsubst %,%.comp.png,$(RECORDINGS))
data/%.avi.comp.png: data/%.avi generate_composite.py
	python generate_composite.py $< $@

CONTOURS = $(patsubst %,%.contours.pkl,$(RECORDINGS))
data/%.avi.contours.pkl: data/%.avi dump_contours.py
	python dump_contours.py $< $@


.PHONY : all
all : $(COMPOSITES) $(CONTOURS)
