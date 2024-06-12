package com.example.smartfarm;

import java.util.UUID;

public class Scheduler {
    public String id;
    public int cycle;
    public int flow1;
    public int flow2;
    public int flow3;
    public boolean isActive;
    public String schedulerName;
    public String startTime;
    public String stopTime;

    public Scheduler(String id, int cycle, int flow1, int flow2, int flow3, boolean isActive, String schedulerName, String startTime, String stopTime) {
        this.id = id;
        this.cycle = cycle;
        this.flow1 = flow1;
        this.flow2 = flow2;
        this.flow3 = flow3;
        this.isActive = isActive;
        this.schedulerName = schedulerName;
        this.startTime = startTime;
        this.stopTime = stopTime;
    }

    // Getters and setters for all fields

    @Override
    public String toString() {
        return "Scheduler{" +
                "id='" + id + '\'' +
                ", cycle=" + cycle +
                ", flow1=" + flow1 +
                ", flow2=" + flow2 +
                ", flow3=" + flow3 +
                ", isActive=" + isActive +
                ", schedulerName='" + schedulerName + '\'' +
                ", startTime='" + startTime + '\'' +
                ", stopTime='" + stopTime + '\'' +
                '}';
    }
}
