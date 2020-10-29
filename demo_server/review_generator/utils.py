class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FakeReviewGenerator(metaclass=Singleton):
    import gpt_2_simple as gpt2

    def __init__(self):
        self.sess = self.gpt2.start_tf_sess()
        self.gpt2.load_gpt2(self.sess, run_name='run2', checkpoint_dir='./static/checkpoint')

    def generate(self, input_text):
        text = self.gpt2.generate(self.sess,
                                  length=300,
                                  temperature=0.7,
                                  prefix="<|startoftext|>" + input_text,
                                  truncate='<|endoftext|>',
                                  checkpoint_dir='./static/checkpoint',
                                  return_as_list=True,
                                  run_name='run2',
                                  include_prefix=False,
                                  top_k=40
                                  )[0]
        return input_text + text
