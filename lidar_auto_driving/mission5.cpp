#include "ros/ros.h"
#include "std_msgs/String.h"
#include "sensor_msgs/LaserScan.h"
#include "geometry_msgs/Twist.h"

float velocity;
float left, fleft,ffleft;
float right,fright,ffright;
float front, back;
float turn;
float flag=0;

void control(float a, float b)
{
  velocity = a;
  turn = b;
}

void scan_Callback(const sensor_msgs::LaserScan::ConstPtr& msg)
{
  left = msg->ranges[269];
  right = msg->ranges[89];
  front = msg->ranges[179];
  fleft = msg->ranges[259];
  fright=msg->ranges[99];
  back = msg->ranges[0];
  ffleft = msg->ranges[239];
  ffright = msg->ranges[119];

  //직선 코스 주행하기(flag 0)
  if(flag == 0)
  {
    if(left < 1.0) {
      if(left > right-0.27) {
        control(0.4,0.2);
      }
      else if (left < right-0.27) {
        control(0.4,-0.2);
      }
      else {
        control(0.2,0);
      }
    }
    else {
      flag++;
    }
  }

  //주차구역 지나도 직선주행(flag 1)
  else if (flag == 1) {
    if(fleft > 0.9)
    {
      control(0.3,0);
    }
    else {
      control(0,0);
      flag++;
    }
  }

  //주차구역 들어가게 차선 맞추기(flag 2)
  else if (flag == 2) {
    if(fleft > 0.5)
    {
      control(0,0.4);
    }
    else {
      control(0,0);
      flag++;
    }
  }

  //주차구역 들어가기(flag 3)
  else if (flag == 3) {
    if(fleft > fright) {
      if(front >= 0.1 && front <= 0.2)
      {
        control(0,0);
        flag++;
      }
      else {
        control(0.15,0.2);
      }
    }
    else if (fleft < fright) {
      if(front >= 0.1 && front <= 0.2)
      {
        control(0,0);
        flag++;
      }
      else {
        control(0.15,-0.2);
      }
    }
    else {
      if(front >= 0.1 && front <= 0.2)
      {
        control(0,0);
        flag++;
      }
      else {
        control(0.2,0);
      }
    }
  }
  //주차구역 빠져나오기(flag 4)
  else if (flag == 4) {
    if(fright < 0.59)
    {
      control(-0.2,0);
    }
    else {
      control(0,0);
      flag++;
    }
  }
  //직선주행으로 맞추기(flag 5)
  else if(flag == 5) {
    if(right > 0.85)
    {
      control(0,-0.4);
    }
    else {
      control(0,0);
      flag++;
    }
  }
  //finish지점까지 가기(flag 6)
  else if (flag == 6) {
    if(fright<=1.2)
    {
      if(fleft > fright+0.01) {
        control(0.5,0.2);
      }
      else if (fleft < fright+0.01) {
        control(0.5,-0.2);
      }
      else {
        control(0.5,0);
      }
    }
    else {
      control(0,0);
      flag++;
    }
  }

  ROS_INFO("fleft diatance : %f m",fleft);
  ROS_INFO("left diatance : %f m",left);
  ROS_INFO("right distance : %f m",right);
 // ROS_INFO("velocity value : %f",velocity);
  ROS_INFO("flag count : %f m",flag);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "bucket_parking");
  ros::NodeHandle nh;

  ros::Subscriber sub = nh.subscribe("/scan", 1000, scan_Callback);
  ros::Publisher cmd_vel_pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel", 1000);

  ros::Rate loop_rate(10);
  while (ros::ok())
  {
    geometry_msgs::Twist msg;

    msg.linear.x = velocity;
    msg.angular.z = turn;

    //ros::Duration(3.0).sleep();

    cmd_vel_pub.publish(msg);

    ros::spinOnce();

    loop_rate.sleep();
  }

  return 0;
}