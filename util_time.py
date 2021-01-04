import time

class TimeUtil:

    @classmethod
    def get_time_stamp(cls):
        """取得当前时间戳"""
        return time.strftime("%Y-%m-%d_%H:%M:%S")

    @classmethod
    def get_time_stamp_reverse(cls):
        """取得当前时间戳"""
        return time.strftime("%H-%M-%S#%Y-%m-%d")

    @classmethod
    def get_date_stamp(cls):
        """取得当前时间戳"""
        return time.strftime("%Y-%m-%d")


if __name__ == '__main__':
    print(TimeUtil.get_time_stamp())
    time.sleep(10)
    print(TimeUtil.get_time_stamp())

