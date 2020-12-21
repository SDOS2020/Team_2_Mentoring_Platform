const Requests = {
	delimiters: ["[[", "]]"],
	template: `
		<ul class="list-group">
			<li class="list-group-item" v-for="request in requests" v-bind:key="request.id">
				<a style="float: left;" href="#">
					[[ request.username ]]
				</a>
				<div align='right'>
					<button v-on:click="acceptRequest(request.username)" class="btn btn-sm btn-success"> Accept </button>
					<button v-on:click="rejectRequest(request.username)" class="btn btn-sm btn-danger"> Reject </button>
				</div>
			</li>
		</ul>
	`,
	data() {
		return {
			requests: []
		};
	},
	created() {
		let request_url = "http://127.0.0.1:8000/api/get_user_requests";

		axios.get(
			request_url
		)
		.then(response => {
			console.log("[SUCCESS]");
			if (response.data.length > 30) {
				console.log("Too many results: " + response.data.length);
				console.log("Showing only top 30");
				this.requests = response.data.slice(0, 30);
			}
			else {
				this.requests = response.data;
			}
		})
		.catch(error => {
			console.log("[ERROR]");
			console.log(error);
			this.requests = [];
		});
	},
	methods: {
		acceptRequest(username) {
			let request_url = "http://127.0.0.1:8000/api/accept_mentorship_request";

			axios.get(
				request_url,
				{
					'params': {
						'requestor': username
					}
				}
			)
			.then(response => {
				console.log("[SUCCESS]");
				this.requests = this.requests.filter(request => request.username !== username);
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});
		},
		rejectRequest(username) {
			let request_url = "http://127.0.0.1:8000/api/reject_mentorship_request";

			axios.get(
				request_url,
				{
					'params': {
						'requestor': username
					}
				}
			)
			.then(response => {
				console.log("[SUCCESS]");
				this.requests = this.requests.filter(request => request.username !== username);
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});
		}
	}
};