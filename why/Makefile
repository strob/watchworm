RECORDINGS = $(wildcard data/*.avi)

COMPOSITES = $(patsubst %,%.comp.png,$(RECORDINGS))
data/%.avi.comp.png: data/%.avi generate_composite.py
	python generate_composite.py $< $@

CONTOURS = $(patsubst %,%.contours.pkl,$(RECORDINGS))
data/%.avi.contours.pkl: data/%.avi dump_contours.py
	python dump_contours.py $< $@

JSONS = Recording.json
$(JSONS) : $(RECORDINGS) jsonification.py
	python jsonification.py

.PHONY : all
all : $(COMPOSITES) $(CONTOURS) $(JSONS)

.PHONY : clean
clean : 
	rm $(COMPOSITES) $(CONTOURS) $(JSONS)
