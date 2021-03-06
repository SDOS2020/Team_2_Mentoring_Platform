const ProgressTracker = {
	delimiters: ["[[", "]]"],
	components: {
	},
	template: `
	<div>
		<div class="card-header" style="border-radius: 10px 10px 0 0; background-color: lightgrey;" id="progress-tracker-header">
			<center>
				<font size="4">
					<b>Progress Tracker</b>
				</font>
			</center>
		</div>

		<div style="height: 71vh; overflow-y: scroll;" id="progress-tracker-body">
			<div v-if="milestones.length === 0" id="no-milestones-text">
				<center style="margin-top: 5rem;">
					Add milestones to track your progress
				</center>
			</div>

			<main>
				<p v-for="milestone in milestones">
					[[ milestone.content ]]
					</br>
					<small class="font-italic" style="color: #7575ab;"> [[ milestone.timestamp ]] </small>
				</p>
			</main>

			
		</div>
	</div>
	`,
	data() {
		return {
			milestones: [],
		};
	},

	props: {
		mentor: null,
		mentee: null,
	},

	created() {
		this.get_milestones();
		window.setInterval(this.get_milestones, 2000);
	},

	methods: {
		get_milestones() {
			let request_url = "/api/get_milestones";
			axios.get(request_url, {'params':{
				'mentor': this.mentor,
				'mentee': this.mentee,
			}})
			.then(response => {
				this.milestones = response.data.milestones;
			})
			.catch(error => {
				console.log('[ERROR]');
				console.log(error);
			});
		}
	}
};
