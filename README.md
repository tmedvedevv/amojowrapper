![amojowrapper](.github/logo.png)

🚀 **amojowrapper** is a Python library designed to interact with the [amoCRM Chat API](https://www.amocrm.ru/developers/content/chats/chat-api-reference). It provides a user-friendly API client for seamless communication with chat channels.

---

## 🛠️ Installation

### Using Poetry

To install using Poetry, run:

```bash
poetry add amojowrapper
```

### Installing from Source

To install the latest version directly from the source:

1. **Clone the repository**:

```bash
git clone https://github.com/tmedvedevv/amojowrapper.git
```

2. **Navigate to the cloned repository**:

```bash
cd amojowrapper
```

3. **Install dependencies and create a virtual environment with Poetry**:

```bash
make install
```

4. **Build the package**:

```bash
make build
```

5. **Install the package**:

```bash
pip install dist/amojowrapper-*.whl --break-system-packages
```

---

## ⚙️ Usage

To start using the library, create an instance of `AmojoClient` by passing the necessary parameters:

```python
from amojowrapper.client import AmojoClient

client = AmojoClient(
    referer="amojo.amocrm.ru",  # amojo.kommo.com (use the appropriate domain)
    amojo_account_token="<amojo_account_token>",  # Account token
    channel_secret="<channel_secret_key>",  # Channel secret key
    channel_id="<channel_amojo_id>",  # Channel ID
    debug=False,  # Enable or disable debugging (default: False)
)
```

Every action performed on a channel is done via an `action` module, located in `amojowrapper/actions`. Each action has its own Pydantic schema for request and response, along with a class that handles the logic of the request.

---

## 📚 Available Actions

| Action                                        | Description                                  |
|-----------------------------------------------|----------------------------------------------|
| [ChannelAction](#ChannelAction)               | Connect or disconnect a chat channel         |
| [ChatAction](#ChatAction)                     | Create a new chat                           |
| [HistoryAction](#HistoryAction)               | Retrieve chat history                        |
| [TypingAction](#TypingAction)                 | Send typing status information              |
| [DeliveryStatusAction](#DeliveryStatusAction) | Update message delivery status              |
| [ReactAction](#ReactAction)                   | Send or remove a reaction                    |
| [MessageAction](#MessageAction)               | Send or edit messages                       |

---

## 📌 Example Usage

### 💻 Channel Connection & Disconnection 
#### ChannelAction

```python
from amojowrapper.actions import ChannelAction

# Create an instance of ChannelAction
channel = ChannelAction(client)

# Connect the channel (optional: 'title' parameter)
channel_response_schema = channel.connect()

# Disconnect the channel
channel.disconnect()
```

---

### 💬 Create a Chat
#### ChatAction

```python
from amojowrapper.actions import ChatAction

# Create an instance of ChatAction
chat = ChatAction(client)

# Parameters for creating a new chat
conversation_id = "identify-8e3e7640-49af-4448-a2c6-d5a421f7f217"
source_external_id = "source_1"
user_id = "identify-1241251234"
user_avatar = "https://avatars.githubusercontent.com/u/47181197?v=4"
user_name = "Some Name"
user_profile_phone = "2412512352"
user_profile_email = "example.client@example.com"

# Create the chat
chat_response = chat.create(
    conversation_id=conversation_id,
    source_external_id=source_external_id,
    user_id=user_id,
    user_avatar=user_avatar,
    user_name=user_name,
    user_profile_phone=user_profile_phone,
    user_profile_email=user_profile_email
)
```

---

### 📜 Retrieve Chat History
#### HistoryAction

```python
from amojowrapper.actions import HistoryAction

# Create an instance of HistoryAction
history = HistoryAction(client)

# Provide the conversation ID (chat reference)
conversation_ref_id = "<chat_id>"

# Retrieve the chat history
history_response = history.get(conversation_ref_id=conversation_ref_id)
```

---

### ⌨️ Send Typing Status
#### TypingAction

```python
from amojowrapper.actions import TypingAction

# Create an instance of TypingAction
typing = TypingAction(client)

# Parameters for sending typing status
conversation_id = "helloworld_test"
sender_id = "new_user-mazharreal"

# Send typing status
typing.send(conversation_id=conversation_id, sender_id=sender_id)
```

---

### 📦 Update Message Delivery Status
#### DeliveryStatusAction

```python
from amojowrapper.actions import DeliveryStatusAction

# Create an instance of DeliveryStatusAction
delivery = DeliveryStatusAction(client)

# Parameters for delivery status update
msgid = "ccc0ccdd-ef14-4d87-9281-5f5656685d3d"
delivery_status = -1  # Example: Error status
error_code = 905  # Error code
error_text = "amojowrapper hello world!"  # Error message text

# Update the delivery status
delivery.set(
    msgid=msgid,
    delivery_status=delivery_status,
    error_code=error_code,
    error=error_text
)
```

---

### 😎 Send Reaction
#### ReactAction

```python
from amojowrapper.actions import ReactAction

# Create an instance of ReactAction
react = ReactAction(client)

# Parameters for sending a reaction
conversation_ref_id = "<amojo_chat_id>"
user_ref_id = "<amojo_user_id>"
message_id = "<message_id>"
reaction_type = "react"  # Reaction type (e.g., "react")
emoji = "👍"  # Emoji for the reaction

# Send the reaction
react.set(
    conversation_ref_id=conversation_ref_id,
    user_ref_id=user_ref_id,
    id=message_id,
    type=reaction_type,
    emoji=emoji
)
```

---

### 📩 Send and Edit Messages
#### MessageAction

#### Sending a Message

```python
from amojowrapper.actions import MessageAction

# Parameters for sending a message
conversation_ref_id = "b6893a27-test-4d49-8710-ba777ce96001"
sender_ref_id = "cb6cf2cb-71e8-test-bd00-5083a5b98a51"
message_type = "text"
message_text = "incoming chat message"

# Create an instance of MessageAction
message = MessageAction(client)

# Send the message
result = message.send(
    message_type=message_type,  # Other possible types are available in the documentation
    message_text=message_text,
    conversation_ref_id=conversation_ref_id,  # If not created, pass as conversation_id
    sender_ref_id=sender_ref_id,  # If not created, pass as sender_id
    silent=True,
    # receiver_ref_id = specify if it's an outgoing message
)
```

#### Editing a Message

```python
from amojowrapper.actions import MessageAction

# Parameters for editing a message
conversation_ref_id = "b6893a27-a78c-4d49-8710-ba777ce96001"
sender_ref_id = "cb6cf2cb-71e8-46db-bd00-5083a5b98a51"
msgid = "amojowrapper_msgid_1ecac67d-64d2-414b-afea-4e274fec4d7e"
message_type = "text"
message_text = "1"

# Create an instance of MessageAction
message = MessageAction(client)

# Edit the message
result = message.edit(
    msgid=msgid,
    message_type=message_type,
    message_text=message_text,
    conversation_ref_id=conversation_ref_id,
    sender_ref_id=sender_ref_id,
    silent=True,
)
```

---

## 🌱 Contributions

Contributions to the library are welcome! If you have suggestions, bug fixes, or ideas for improvement, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature.
3. Make changes and commit them.
4. Push your changes to your fork.
5. Create a Pull Request.

### 🧪 Testing

The library includes tests written with `pytest`. To run the tests:

1. Ensure test data is prepared within each test.
2. Run the tests:

    ```bash
    make test
    ```

   For debugging:

   ```bash
   make test-debug
   ```

---

To view other available commands for the project, run:

```bash
make help
```

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.