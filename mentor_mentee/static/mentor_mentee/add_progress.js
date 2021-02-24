const AddProgress = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<center>
			<button style="background-color: #7474aa; color: white;" class="btn btn-block" data-toggle="modal" data-target="#addProgressModal" data-whatever="@mdo">
				Add Milestone
			</button>
		</center>

		<div class="modal fade" id="addProgressModal" tabindex="-1" role="dialog" aria-labelledby="addProgressModalLabel" aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content">

					<div class="modal-header">
						<h5 class="modal-title" id="addProgressModalLabel">
							Add a milestone
						</h5>
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>

					<div class="modal-body">
						<form>
							<div class="form-group">
								<label class="col-form-label">Enter details:</label>
								<textarea v-model="new_milestone" class="form-control"></textarea>
							</div>
						</form>
					</div>

					<div class="modal-footer">
						<button v-on:click="add_new_meeting" class="btn btn-success">Add Milestone</button>
						<button id="add_milestone-close-button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>
				</div>
			</div>
		</div>
	</div>
	`,
	
	data() {
		return {
			new_milestone: "",
		};
	},

	props: {
		mentor: {
			required: true
		},
		mentee: {
			required: true
		},
		csrf: {
			required: true
		},
	},

	methods: {

		add_new_meeting() {
			let request_url = "/api/add_milestone/";

			axios.post(request_url, {
				'mentor': this.mentor,
				'mentee': this.mentee,
				'content': this.new_milestone,
			}, {
				headers: {
					'X-CSRFTOKEN': this.csrf
				}
			})
			.then(response => {
			})
			.catch(error => {
				console.log('[ERROR]');
				console.log(error);
			});

			this.new_milestone = "";

			document.getElementById("add_milestone-close-button").click();
		}
	}
};
