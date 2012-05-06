#!/bin/sh

sudo pip uninstall flashcards
sudo rm /usr/local/lib/python2.7/dist-packages/flashcards/*
sudo rm /usr/local/lib/python2.7/dist-packages/flashcards-2.3-py2.7.egg-info/*

sudo rmdir /usr/local/lib/python2.7/dist-packages/flashcards
sudo rmdir /usr/local/lib/python2.7/dist-packages/flashcards-2.3-py2.7.egg-info

sudo rm /usr/local/bin/flashcards

sudo rm ~/Documents/flashcards/*
sudo rmdir ~/Documents/flashcards

rm ~/.flashcards/*
rmdir ~/.flashcards

