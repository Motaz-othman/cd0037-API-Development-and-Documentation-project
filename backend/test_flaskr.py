import unittest
from flaskr import create_app
from models import setup_db, db, Question, Category  # import models!
import os

TEST_DB_URI = os.getenv("DATABASE_URL", "postgresql:///trivia_test")

class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        print("Hi")  # <-- will print once a test runs
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": TEST_DB_URI,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True,
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            print("DB URL ->", db.engine.url)
            print("Tables ->", db.inspect(db.engine).get_table_names())
            names = ["Science","Art","Geography","History","Entertainment","Sports"]
            for n in names:
                db.session.add(Category(type=n))
            db.session.commit()

            # Seed questions (category is STRING of category id)
            seed_qs = [
                Question(question="What is H2O?", answer="Water", category="1", difficulty=1),
                Question(question="What planet is red?", answer="Mars", category="1", difficulty=1),
                Question(question="Capital of France?", answer="Paris", category="3", difficulty=1),
                Question(question="WWII ended in?", answer="1945", category="4", difficulty=2),
                Question(question='Who directed "Inception"?', answer="Christopher Nolan", category="5", difficulty=2),
                Question(question="How many soccer players on field?", answer="11", category="6", difficulty=1),
            ]
            db.session.add_all(seed_qs)
            db.session.commit()

            # Keep for tests
            self.total_seed = Question.query.count()
    def tearDown(self):

        pass

    def test_get_categories_ok(self):
        res = self.client.get("/categories")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("categories", data)
        self.assertIsInstance(data["categories"], dict)


    def test_get_questions_first_page_ok(self):
        res = self.client.get("/questions?page=1")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("questions", data)
        self.assertIn("total_questions", data)
        self.assertIn("categories", data)


    def test_get_questions_out_of_range_404(self):
        res = self.client.get("/questions?page=9999")
        self.assertEqual(res.status_code, 404)
        data = res.get_json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)

    def test_create_question_201_ok(self):
        new_q = {
            "question": "Who painted the Mona Lisa?",
            "answer": "Leonardo da Vinci",
            "category": "2",
            "difficulty": 2
        }
        res = self.client.post("/questions", json=new_q)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("created", data)
        self.assertIn("question", data)


    def test_create_question_400_missing_fields(self):
        bad_q = {"question": "Incomplete", "answer": "X"}  
        res = self.client.post("/questions", json=bad_q)
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 400)


    def test_search_questions_ok(self):
        res = self.client.post("/questions", json={"searchTerm": "capital"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("questions", data)

        self.assertTrue(any("Capital of France" in q["question"] for q in data["questions"]))
        self.assertIn("total_questions", data)
        self.assertIsNone(data["current_category"])


    def test_delete_question_ok_then_404(self):

        with self.app.app_context():
            q = Question(question="Temp Q", answer="A", category="1", difficulty=1)
            q.insert()
            qid = q.id

        res = self.client.delete(f"/questions/{qid}")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["deleted_question"], qid)


        res2 = self.client.delete(f"/questions/{qid}")
        self.assertEqual(res2.status_code, 404)


    def test_get_questions_by_category_ok(self):

        res = self.client.get("/categories/1/questions")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("questions", data)
        self.assertGreaterEqual(data["total_questions"], 2)
        self.assertEqual(data["current_category"], 1)
 
        self.assertTrue(all(q["category"] == "1" for q in data["questions"]))

    def test_get_questions_by_category_404_nonexistent_category(self):
        res = self.client.get("/categories/9999/questions")
        self.assertEqual(res.status_code, 404)
        data = res.get_json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)


    def test_quizzes_all_respects_previous(self):
        res1 = self.client.post("/quizzes", json={"previous_questions": [], "quiz_category": {"id": 0}})
        self.assertEqual(res1.status_code, 200)
        q1 = res1.get_json()["question"]
        self.assertTrue(q1 is None or "id" in q1)

        if q1:

            res2 = self.client.post("/quizzes", json={"previous_questions": [q1["id"]], "quiz_category": {"id": 0}})
            self.assertEqual(res2.status_code, 200)
            q2 = res2.get_json()["question"]
            self.assertTrue(q2 is None or q2["id"] != q1["id"])

    def test_quizzes_filtered_category(self):

        res = self.client.post("/quizzes", json={"previous_questions": [], "quiz_category": {"id": 1}})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        q = data["question"]

        self.assertIsNotNone(q)
        self.assertEqual(q["category"], "1")

if __name__ == "__main__":
    unittest.main(verbosity=2)
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
