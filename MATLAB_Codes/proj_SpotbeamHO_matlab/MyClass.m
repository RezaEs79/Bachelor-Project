classdef MyClass
    properties
        id
        rss
        capacity
        height
        memory
        
    end
    
    methods
        function obj = MyClass(id,rss,capacity,height,memory)
            obj.id = id;
            obj.rss = rss;
            obj.capacity = capacity;
            obj.height = height;
            obj.memory = memory;
        end
    end
end
