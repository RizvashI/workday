# Launch Template for EC2 instances used in the Auto Scaling Group
resource "aws_launch_template" "bulls_app" {
  name_prefix   = "bulls-launch-"
  image_id      = "ami-009082a6cd90ccd0e" # Amazon Linux 2023 (eu-central-1)
  instance_type = "t3.micro"
  user_data     = base64encode(file("${path.module}/userdata.sh"))

  # Define the security group for the EC2 instance
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "bulls-app"
    }
  }
}

# Auto Scaling Group definition with a fixed instance count
resource "aws_autoscaling_group" "bulls_asg" {
  desired_capacity          = 1
  max_size                  = 1
  min_size                  = 1
  vpc_zone_identifier       = [aws_subnet.public.id]
  health_check_type         = "EC2"
  health_check_grace_period = 30

  # Link to launch template
  launch_template {
    id      = aws_launch_template.bulls_app.id
    version = "$Latest"
  }

  # Tag propagated to launched instances
  tag {
    key                 = "Name"
    value               = "bulls-asg"
    propagate_at_launch = true
  }

  # Ensures new instances are created before old ones are destroyed
  lifecycle {
    create_before_destroy = true
  }
}

# CloudWatch alarm for high CPU usage (not wired to scale out yet)
resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "HighCPU"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 120
  statistic           = "Average"
  threshold           = 60
  alarm_description   = "Alarm when CPU exceeds 60%"
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.bulls_asg.name
  }

  # Optional: Add action (SNS, Lambda, scaling policy)
  alarm_actions = []
}

# Output name of the Auto Scaling Group
output "asg_name" {
  value = aws_autoscaling_group.bulls_asg.name
}
