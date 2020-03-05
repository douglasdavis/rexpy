CXXFLAGS = $(shell root-config --cflags) -Iinclude -g0 -O3
LDFLAGS = $(shell root-config --libs) -lz
TARGET = augment-tree-with-npy

$(TARGET): $(TARGET).cpp
	$(CXX) -o $@ $(CXXFLAGS) $< $(LDFLAGS)

.PHONY: clean

clean:
	$(RM) $(TARGET)
