def path_extend():
    import sys
    import os

    current_dir = "/home/devna0111/rag_chatbot"
    
    # 최상위 폴더 먼저 추가
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    folder_list = [
        name for name in os.listdir(current_dir)
        if os.path.isdir(os.path.join(current_dir, name)) and not name.startswith('.')
    ]
    
    for module in folder_list:
        sub_dir = os.path.join(current_dir, module)
        if sub_dir not in sys.path:
            sys.path.insert(0, sub_dir)
