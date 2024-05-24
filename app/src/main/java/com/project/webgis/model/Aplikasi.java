package com.project.webgis.model;

public class Aplikasi {
    int id;
    String afdeling;
    String block;
    String targetTonase;
    String targetPokok;
    String progressTonase;
    String progressPokok;
    String sph;
    String progress;
    String date;

    public Aplikasi() {

    }

    public Aplikasi(int id, String afdeling, String block, String targetTonase, String targetPokok, String progressTonase, String progressPokok, String sph, String progress, String date) {
        this.id = id;
        this.afdeling = afdeling;
        this.block = block;
        this.targetTonase = targetTonase;
        this.targetPokok = targetPokok;
        this.progressTonase = progressTonase;
        this.progressPokok = progressPokok;
        this.sph = sph;
        this.progress = progress;
        this.date = date;
    }

    public int getId() {
        return id;
    }

    public String getAfdeling() {
        return afdeling;
    }

    public String getBlock() {
        return block;
    }

    public String getTargetTonase() {
        return targetTonase;
    }

    public String getTargetPokok() {
        return targetPokok;
    }

    public String getProgressTonase() {
        return progressTonase;
    }

    public String getProgressPokok() {
        return progressPokok;
    }

    public String getSph() {
        return sph;
    }

    public String getProgress() {
        return progress;
    }

    public String getDate() {
        return date;
    }
}
