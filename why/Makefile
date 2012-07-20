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
PATHS45P = $(patsubst %,%.pathADP45.png,$(RECORDINGS))
data/%.avi.pathADP45.pkl: paths.py data/%.avi.contoursADP45.pkl data/%.avi.contoursADP45.png
	python $^ $@

MOT45 = $(patsubst %,%.showmotionADP45.webm,$(RECORDINGS))
data/%.avi.showmotionADP45.webm: showmotion.py data/%.avi.contoursADP45.webm data/%.avi.pathADP45.pkl
	python $^ $@

CONTOUR60 = $(patsubst %,%.contoursMOT60.pkl,$(RECORDINGS))
CONTOUR60P = $(patsubst %,%.contoursMOT60.png,$(RECORDINGS))
data/%.avi.contoursMOT60.pkl: contours60.py data/%.avi data/%.avi.comp.png
	python $^ $@

PATHS60 = $(patsubst %,%.pathMOT60.pkl,$(RECORDINGS))
PATHS60P = $(patsubst %,%.pathMOT60.png,$(RECORDINGS))
data/%.avi.pathMOT60.pkl: paths.py data/%.avi.contoursMOT60.pkl data/%.avi.contoursMOT60.png
	python $^ $@

MOT60 = $(patsubst %,%.showmotionMOT60.webm,$(RECORDINGS))
data/%.avi.showmotionMOT60.webm: showmotion.py data/%.avi.contoursMOT60.webm data/%.avi.pathMOT60.pkl
	python $^ $@


CONTOUR50 = $(patsubst %,%.contoursMBL50.pkl,$(RECORDINGS))
CONTOUR50P = $(patsubst %,%.contoursMBL50.png,$(RECORDINGS))
data/%.avi.contoursMBL50.pkl: contours50.py data/%.avi data/%.avi.comp.png
	python $^ $@


PATHS50 = $(patsubst %,%.pathMBL50.pkl,$(RECORDINGS))
PATHS50P = $(patsubst %,%.pathMBL50.png,$(RECORDINGS))
data/%.avi.pathMBL50.pkl: paths.py data/%.avi.contoursMBL50.pkl data/%.avi.contoursMBL50.png
	python $^ $@

MOT50 = $(patsubst %,%.showmotionMBL50.webm,$(RECORDINGS))
data/%.avi.showmotionMBL50.webm: showmotion.py data/%.avi.contoursMBL50.webm data/%.avi.pathMBL50.pkl
	python $^ $@

CONTOUR75 = $(patsubst %,%.contoursMBL75.pkl,$(RECORDINGS))
CONTOUR75P = $(patsubst %,%.contoursMBL75.png,$(RECORDINGS))
data/%.avi.contoursMBL75.pkl: contours75.py data/%.avi data/%.avi.comp.png
	python $^ $@

PATHS75 = $(patsubst %,%.pathMBL75.pkl,$(RECORDINGS))
PATHS75P = $(patsubst %,%.pathMBL75.png,$(RECORDINGS))
data/%.avi.pathMBL75.pkl: paths.py data/%.avi.contoursMBL75.pkl data/%.avi.contoursMBL75.png
	python $^ $@

MOT75 = $(patsubst %,%.showmotionMBL75.webm,$(RECORDINGS))
data/%.avi.showmotionMBL75.webm: showmotion.py data/%.avi.contoursMBL75.webm data/%.avi.pathMBL75.pkl
	python $^ $@

JSONS = Recording.json
$(JSONS) : $(RECORDINGS) jsonification.py $(PATHS45) $(PATHS50) $(PATHS60) $(PATHS75)
	python jsonification.py

GEN = $(COMPOSITES) $(CONTOUR45) $(CONTOUR45P) $(CONTOUR60) $(CONTOUR60P) \
      $(CONTOUR50) $(CONTOUR50P) $(CONTOUR75) $(CONTOUR75P) \
      $(MOT45) $(MOT50) $(MOT60) $(MOT75) \
      $(JSONS) $(FIRSTFRAMES) $(WEBMS) \
      $(PATHS45) $(PATHS45P) $(PATHS60) $(PATHS60P) $(PATHS50) $(PATHS50P) $(PATHS75) $(PATHS75P)

.PHONY : clean
clean : 
	rm $(GEN)

.PHONY : all
all : $(GEN)

