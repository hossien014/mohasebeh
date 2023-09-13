class _time_:
      def __init__(self ,hour:int , minute:int) -> None:
            if minute>60 :
                  raise "minute should be under 60"
            self.minute=minute
            self.hour=hour

class work:
      def __init__(self , name:str , time:_time_=None , catgorey:str="") -> None:
            self.name=name
            self.time=time
            self.catgorey=catgorey
            
            
