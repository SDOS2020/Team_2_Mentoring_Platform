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

							<div class="form-group">
								<label for="milestone-time" class="col-form-label">Time:</label>
								<br/>
								<input v-model="milestone_time" type="date" class="form-control" id="milestone-time" name="milestone-time" max="" required>
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
			milestone_time: "",
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

	mounted() {
		var today = new Date();
		var dd = today.getDate();
		var mm = today.getMonth()+1; //January is 0!
		var yyyy = today.getFullYear();
		if (dd < 10) {
				dd ='0'+ dd
		}

		if (mm < 10) {
			mm = '0' + mm
		} 

		today = yyyy + '-' + mm + '-' + dd;
		this.milestone_time = today;
		document.getElementById("milestone-time").setAttribute("max", today);
	},

	methods: {

		add_new_meeting() {
			if (this.new_milestone == "" || this.new_milestone == "") {
				alert("Please fill all the details.")
				return;
			}
			
			let request_url = "/api/add_milestone/";

			axios.post(request_url, {
				'mentor': this.mentor,
				'mentee': this.mentee,
				'content': this.new_milestone,
				'timestamp': this.milestone_time
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
