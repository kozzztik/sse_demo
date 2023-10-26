var app = new Vue({
    el: '#vue_app',
    data: {
        messages: [],
        name: 'message',
        message_text: 'foobar',
        source: null,
    },
    methods: {
        send_message() {
            axios.post(
                '/sse/',
                {name: this.name, data: this.message_text}
            ).then(response => {
                this.message_text = '';
            });
        },
    },
    mounted() {
        this.source = new EventSource("/sse/");
        this.source.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.messages.push({
                id: event.lastEventId,
                name: event.type,
                data: event.data
            });
        };
    },
});

