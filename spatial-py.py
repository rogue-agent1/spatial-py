#!/usr/bin/env python3
"""Spatial index: quadtree for 2D point queries."""
import sys

class Rect:
    def __init__(self,x,y,w,h):self.x,self.y,self.w,self.h=x,y,w,h
    def contains(self,px,py):return self.x<=px<self.x+self.w and self.y<=py<self.y+self.h
    def intersects(self,other):
        return not(other.x>=self.x+self.w or other.x+other.w<=self.x or other.y>=self.y+self.h or other.y+other.h<=self.y)

class QuadTree:
    def __init__(self,boundary,capacity=4):
        self.boundary=boundary;self.capacity=capacity;self.points=[];self.divided=False;self.children=[]
    def insert(self,x,y,data=None):
        if not self.boundary.contains(x,y):return False
        if len(self.points)<self.capacity and not self.divided:
            self.points.append((x,y,data));return True
        if not self.divided:self._subdivide()
        for child in self.children:
            if child.insert(x,y,data):return True
        return False
    def _subdivide(self):
        b=self.boundary;hw,hh=b.w/2,b.h/2
        self.children=[QuadTree(Rect(b.x,b.y,hw,hh),self.capacity),
                       QuadTree(Rect(b.x+hw,b.y,hw,hh),self.capacity),
                       QuadTree(Rect(b.x,b.y+hh,hw,hh),self.capacity),
                       QuadTree(Rect(b.x+hw,b.y+hh,hw,hh),self.capacity)]
        self.divided=True
        for p in self.points:
            for c in self.children:c.insert(*p)
        self.points=[]
    def query(self,rect):
        results=[]
        if not self.boundary.intersects(rect):return results
        for x,y,d in self.points:
            if rect.contains(x,y):results.append((x,y,d))
        if self.divided:
            for c in self.children:results.extend(c.query(rect))
        return results

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        qt=QuadTree(Rect(0,0,100,100),4)
        for i in range(50):qt.insert(i*2,i*2,f"p{i}")
        r=qt.query(Rect(10,10,20,20))
        assert len(r)>0
        assert all(10<=x<30 and 10<=y<30 for x,y,_ in r)
        # Point outside boundary
        assert not qt.insert(200,200)
        # Empty query
        assert qt.query(Rect(200,200,10,10))==[]
        print("All tests passed!")
    else:
        qt=QuadTree(Rect(0,0,100,100))
        for i in range(20):qt.insert(i*5,i*5,i)
        print(f"Query [20,20,30,30]: {qt.query(Rect(20,20,30,30))}")
if __name__=="__main__":main()
