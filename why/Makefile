RECORDINGS = $(wildcard data/*.avi)

# COMPOSITES = $(patsubst %,%.comp.png,$(RECORDINGS))
# data/%.avi.comp.png: generate_composite.py data/%.avi
# 	python $^ $@

WEBMS = $(patsubst %,%.webm,$(RECORDINGS))
data/%.avi.webm: webm.py data/%.avi
	python $^ $@

FIRSTFRAMES = $(patsubst %,%.first.png,$(RECORDINGS))
data/%.avi.first.png: first_frame.py data/%.avi 
	python $^ $@

CONTOURS = $(patsubst %,%.contours.pkl,$(RECORDINGS))
data/%.avi.contours.pkl: ruledcontour.py data/%.avi RULES.json 
	python $^ $@

PATHS = $(patsubst %,%.path.pkl,$(RECORDINGS))
data/%.avi.path.pkl: paths.py data/%.avi.contours.pkl data/%.avi.contours.png
	python $^ $@

MOT = $(patsubst %,%.showmotion.webm,$(RECORDINGS))
data/%.avi.showmotion.webm: showmotion.py data/%.avi data/%.avi.contours.webm data/%.avi.path.pkl
	python $^ $@

JSONS = Recording.json
$(JSONS) : jsonification.py $(RECORDINGS) $(PATHS)
	python $^ $@

CSV = Path.json
$(CSV) : makecsv.py Path.json
	python $^ $@

GEN = $(COMPOSITES) $(CONTOURS) $(MOT) \
      $(JSONS) $(FIRSTFRAMES) $(WEBMS) \
      $(PATHS)

.PHONY : clean
clean : 
	rm $(GEN)

.PHONY : all
all : $(GEN)

