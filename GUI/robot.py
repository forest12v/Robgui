from fanucpy import Robot
class Motion:
    def __init__(self):
        self.robot = Robot(
        robot_model="Fanuc",
        host="127.0.0.1",
        port=18735,
        ee_DO_type="RDO",
        ee_DO_num=7,
        )
        self.robot.connect()
        if self.robot.gripper == True:
            self.robot.gripper(False)

    def Moving(self,axis,mode="joint"):
        self.robot.move(mode,axis)

    def turn_gripper(self,mode):
        self.robot.gripper(mode)
        print(f'gripper - {mode}')