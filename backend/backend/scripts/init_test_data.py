"""初始化测试数据"""
import sys
sys.path.insert(0, '/var/www/training-platform/backend/backend')

from sqlalchemy.orm import Session
from config.database import engine, Base
from models.user import User, UserRole
from models.certificate import Certificate, CertificateLevel, CertificateType, UserCertificate
from models.question import Question, QuestionBank, UserQuestion, WrongQuestion
from models.course import Course, CourseType, CourseOrder
from models.community import CommunityCategory, CommunityPost

from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    """初始化数据库"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    db = Session(bind=engine)
    
    try:
        # 1. 创建证书
        print("创建证书...")
        certificates = [
            {"name": "Java 程序员认证", "code": "JAVA-001", "type": CertificateType.PROFESSIONAL, "level": CertificateLevel.BASIC, "category": "软件开发"},
            {"name": "Java 高级开发", "code": "JAVA-002", "type": CertificateType.PROFESSIONAL, "level": CertificateLevel.INTERMEDIATE, "category": "软件开发"},
            {"name": "Java 架构师", "code": "JAVA-003", "type": CertificateType.PROFESSIONAL, "level": CertificateLevel.ADVANCED, "category": "软件开发"},
            {"name": "Python 开发工程师", "code": "PY-001", "type": CertificateType.PROFESSIONAL, "level": CertificateLevel.BASIC, "category": "软件开发"},
            {"name": "Python 数据分析师", "code": "PY-002", "type": CertificateType.SKILL, "level": CertificateLevel.INTERMEDIATE, "category": "数据分析"},
        ]
        
        cert_map = {}
        for cert_data in certificates:
            cert = Certificate(**cert_data, description=f"{cert_data['name']}认证考试", requirements="完成相关课程并通过考试")
            db.add(cert)
            cert_map[cert_data['code']] = cert
        
        db.commit()
        print(f"✓ 创建 {len(certificates)} 个证书")
        
        # 2. 创建题库
        print("创建题库...")
        question_banks = [
            {"name": "Java 基础题库", "code": "QB-JAVA-001", "certificate_id": cert_map["JAVA-001"].id, "description": "Java 语言基础知识点"},
            {"name": "Java 进阶题库", "code": "QB-JAVA-002", "certificate_id": cert_map["JAVA-002"].id, "description": "Java 高级特性"},
            {"name": "Python 基础题库", "code": "QB-PY-001", "certificate_id": cert_map["PY-001"].id, "description": "Python 编程基础"},
            {"name": "数据分析题库", "code": "QB-PY-002", "certificate_id": cert_map["PY-002"].id, "description": "数据分析与处理"},
        ]
        
        bank_map = {}
        for bank_data in question_banks:
            bank = QuestionBank(**bank_data)
            db.add(bank)
            db.commit()
            db.refresh(bank)
            bank_map[bank_data['code']] = bank
        
        print(f"✓ 创建 {len(question_banks)} 个题库")
        
        # 3. 创建测试题目
        print("创建题目...")
        sample_questions = [
            {"question_bank_id": bank_map["QB-JAVA-001"].id, "content": "Java 中哪个关键字用于继承类？", "options": [{"key": "A", "value": "extends"}, {"key": "B", "value": "implements"}, {"key": "C", "value": "inherits"}, {"key": "D", "value": "uses"}], "answer": "A", "answer_type": "single", "difficulty": "easy", "tags": ["基础", "继承"], "explanation": "Java 中使用 extends 关键字实现类继承"},
            {"question_bank_id": bank_map["QB-JAVA-001"].id, "content": "Java 的基本数据类型包括哪些？", "options": [{"key": "A", "value": "int, float, double, boolean"}, {"key": "B", "value": "String, Integer, Double"}, {"key": "C", "value": "Object, Class"}, {"key": "D", "value": "Array, List"}], "answer": "A", "answer_type": "single", "difficulty": "easy", "tags": ["基础", "数据类型"], "explanation": "Java 基本数据类型包括 int, float, double, boolean, char, byte, short, long"},
            {"question_bank_id": bank_map["QB-JAVA-001"].id, "content": "以下哪些是 Java 访问修饰符？", "options": [{"key": "A", "value": "public"}, {"key": "B", "value": "private"}, {"key": "C", "value": "protected"}, {"key": "D", "value": "static"}], "answer": "A,B,C", "answer_type": "multiple", "difficulty": "medium", "tags": ["基础", "修饰符"], "explanation": "Java 访问修饰符包括 public, private, protected, static 不是访问修饰符"},
            {"question_bank_id": bank_map["QB-PY-001"].id, "content": "Python 中用于定义函数的关键字是？", "options": [{"key": "A", "value": "function"}, {"key": "B", "value": "def"}, {"key": "C", "value": "define"}, {"key": "D", "value": "func"}], "answer": "B", "answer_type": "single", "difficulty": "easy", "tags": ["基础", "函数"], "explanation": "Python 使用 def 关键字定义函数"},
            {"question_bank_id": bank_map["QB-PY-001"].id, "content": "Python 的列表推导式正确语法是？", "options": [{"key": "A", "value": "[x for x in range(10)]"}, {"key": "B", "value": "for x in range(10)"}, {"key": "C", "value": "list(x for x in range(10))"}, {"key": "D", "value": "{x for x in range(10)}"}], "answer": "A", "answer_type": "single", "difficulty": "medium", "tags": ["基础", "列表"], "explanation": "列表推导式使用方括号 []"},
        ]
        
        for q_data in sample_questions:
            question = Question(**q_data)
            db.add(question)
        
        db.commit()
        print(f"✓ 创建 {len(sample_questions)} 道题目")
        
        # 4. 创建社区分类
        print("创建社区分类...")
        categories = [
            {"name": "学习讨论", "description": "学习交流、问题讨论", "icon": "📚"},
            {"name": "经验分享", "description": "学习经验、面试经验", "icon": "💡"},
            {"name": "资源分享", "description": "学习资料、工具推荐", "icon": "📁"},
            {"name": "灌水专区", "description": "自由交流", "icon": "💬"},
        ]
        
        for cat_data in categories:
            category = CommunityCategory(**cat_data)
            db.add(category)
        
        db.commit()
        print(f"✓ 创建 {len(categories)} 个社区分类")
        
        # 5. 创建测试帖子
        print("创建测试帖子...")
        demo_user = db.query(User).filter(User.username == "demo").first()
        if demo_user:
            posts = [
                {"title": "Java 学习路线分享", "content": "大家好，今天分享一下 Java 学习路线...\n\n1. Java 基础\n2. 面向对象\n3. 集合框架\n4. IO 流\n5. 多线程\n\n欢迎大家补充！", "author_id": demo_user.id, "category_id": 1, "tags": "Java,学习路线"},
                {"title": "Python 数据分析入门", "content": "Python 数据分析需要掌握：\n- NumPy\n- Pandas\n- Matplotlib\n- Scikit-learn\n\n有问题的可以留言~", "author_id": demo_user.id, "category_id": 1, "tags": "Python,数据分析"},
                {"title": "面试经验分享", "content": "刚拿到几个 offer，分享一下面试经验...\n\n技术面主要问：\n1. 基础概念\n2. 项目经验\n3. 算法题\n\n祝大家面试顺利！", "author_id": demo_user.id, "category_id": 2, "tags": "面试，经验"},
            ]
            
            for post_data in posts:
                post = CommunityPost(**post_data)
                db.add(post)
            
            db.commit()
            print(f"✓ 创建 {len(posts)} 个帖子")
        
        # 6. 创建测试课程
        print("创建测试课程...")
        courses = [
            {"title": "Java 从入门到精通", "subtitle": "零基础学 Java", "course_type": "recorded", "certificate_id": cert_map["JAVA-001"].id, "description": "完整的 Java 学习课程", "price": 299.0, "original_price": 599.0, "duration": 1200, "tags": ["Java", "编程", "入门"]},
            {"title": "Python 数据分析实战", "subtitle": "掌握数据分析技能", "course_type": "recorded", "certificate_id": cert_map["PY-002"].id, "description": "Python 数据分析完整课程", "price": 399.0, "original_price": 799.0, "duration": 1500, "tags": ["Python", "数据分析"]},
            {"title": "Java 架构师直播课", "subtitle": "每周直播", "course_type": "live", "certificate_id": cert_map["JAVA-003"].id, "description": "高级 Java 架构设计", "price": 999.0, "original_price": 1999.0, "duration": 180, "tags": ["Java", "架构", "直播"]},
        ]
        
        for course_data in courses:
            course = Course(**course_data, status="published")
            db.add(course)
        
        db.commit()
        print(f"✓ 创建 {len(courses)} 个课程")
        
        print("\n========================================")
        print("✅ 测试数据初始化完成！")
        print("========================================")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
