package com.project.webgis.model;

public class Planted {
    int id;
    String afdeling;
    String block;
    String sap;
    String ha;
    String year;
    String level1;
    String level2;
    String status;

    public Planted() {

    }

    public Planted(int id, String afdeling, String block, String sap, String ha, String year, String level1, String level2, String status) {
        this.id = id;
        this.afdeling = afdeling;
        this.block = block;
        this.sap = sap;
        this.ha = ha;
        this.year = year;
        this.level1 = level1;
        this.level2 = level2;
        this.status = status;
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

    public String getHa() {
        return ha;
    }

    public String getLevel1() {
        return level1;
    }

    public String getLevel2() {
        return level2;
    }

    public String getSap() {
        return sap;
    }

    public String getStatus() {
        return status;
    }

    public String getYear() {
        return year;
    }
}
