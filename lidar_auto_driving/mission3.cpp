#include "ros/ros.h"
#include "std_msgs/String.h"
#include "sensor_msgs/LaserScan.h"
#include "geometry_msgs/Twist.h"

float velocity;
float left, right, front;
float turn;
float lmax, lmin, i;
float rmax, rmin, j;

void control(float a, float b)
{
  velocity = a;
  turn = b;
}

void wall_Callback(const sensor_msgs::LaserScan::ConstPtr& msg)
{
  //왼쪽 거리값 최대값, 최소값 설정
  lmax = lmin = msg->ranges[229];
  for(i=230; i<270; i++)
  {
      if(msg->ranges[i] > lmax) lmax = msg->ranges[i];
      if(msg->ranges[i] < lmin) lmin = msg->ranges[i];

  }

  //오른쪽 거리값 최대값, 최소값 설정
  rmax = rmin = msg->ranges[89];
  for(j=90; j<130; j++)
  {
      if(msg->ranges[j] > rmax) rmax = msg->ranges[j];
      if(msg->ranges[j] < rmin) rmin = msg->ranges[j];

  }
  if(lmin<=rmin)
  {
    //직진
    if(lmin < 0.8 && lmin >= 0.6)
    {
      control(0.3,0);
    }

    //우회전
    else if(lmin < 0.6)
    {
      control(0.25,-0.4);
    }

    //좌회전
    else if (lmin >= 0.8 && lmin < 1.5) {
      control(0.25,0.4);
    }

    //도착지점에서 정지
    else {
      control(0,0);
    }
    ROS_INFO("left minimum : %f m",lmin);
  }

  else{
    //직진
    if(rmin < 0.795 && rmin >= 0.6)
    {
      control(0.3,0);
    }

    //좌회전
    else if(rmin < 0.6)
    {
      control(0.25,0.4);
    }

    //우회전
    else if (rmin >= 0.795 && rmin < 1.5) {
      control(0.25,-0.4);
    }

    //도착지점에서 정지
    else {
      control(0,0);
    }
    ROS_INFO("right minimum : %f m",rmin);
  }
  ROS_INFO("velocity value : %f",velocity);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "wall_following2");
  ros::NodeHandle nh;

  ros::Subscriber sub = nh.subscribe("/scan", 1000, wall_Callback);
  ros::Publisher cmd_vel_pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel", 1000);

  ros::Rate loop_rate(10);
  while (ros::ok())
  {
    geometry_msgs::Twist msg;

    msg.linear.x = velocity;
    msg.angular.z = turn;

    cmd_vel_pub.publish(msg);

    ros::spinOnce();

    loop_rate.sleep();
  }

  return 0;
}