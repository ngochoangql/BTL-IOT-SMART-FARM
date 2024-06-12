package com.example.smartfarm;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class AddSchedule extends AppCompatActivity {

    EditText name,cycles,flow1,flow2,flow3,startTime,stopTime;
    Button add;
    MqttHelper mqttHelper;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_add_schedule);
        name = findViewById(R.id.name);
        cycles = findViewById(R.id.cycles);
        flow1 = findViewById(R.id.flow1);
        flow2 = findViewById(R.id.flow2);
        flow3 = findViewById(R.id.flow3);
        startTime = findViewById(R.id.startTime);
        stopTime = findViewById(R.id.stopTime);
        add = findViewById(R.id.button);
        mqttHelper = new MqttHelper("smart-farm",this);
        add.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mqttHelper.publish("add-schedule","{" +
                        "\"schedulerName\":\" " + name.getText()+"\","+
                        "\"cycle\": " + cycles.getText()+","+
                        "\"flow1\": " + flow1.getText()+","+
                        "\"flow2\": " + flow2.getText()+","+
                        "\"flow3\": " + flow3.getText()+","+
                        "\"isActive\": true,"+
                        "\"startTime\": \"" + startTime.getText()+"\","+
                        "\"stopTime\": \"" + stopTime.getText()+"\""+"}",0,false);
                Toast.makeText(AddSchedule.this,"Add success",Toast.LENGTH_SHORT).show();

                Intent intent = new Intent(AddSchedule.this, MainActivity.class);
                startActivity(intent);
                finish();
            }

        });


    }
}