import faust
from faker import Faker

faker = Faker()


class Greeting(faust.Record):
    from_name: str
    to_name: str
    
app = faust.App("hello-app", broker="kafka://localhost:29092")
topic = app.topic("hello-topic", value_type=Greeting)

@app.agent(topic)
async def hello(greetings):
    async for greeting in greetings:
        print(f"Hello from {greeting.from_name} to {greeting.to_name}")
        
@app.timer(interval=1.0)
async def example_sender(app):
    await hello.send(
        value=Greeting(from_name="Faust", to_name=faker.name())
    )
    
if __name__ == "__main__":
    app.main()