%Intiailize EEGLAB
cd ~; cd eeglab13_6_5b/;
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
filename = 'new1'
channel_idx = [1 2 3 4 5 6 7 8];
%Import XDF File
FILE = ['/home/ibagon/Documents/Research/RL_BCI/data/' filename '/' filename '.xdf'];
EEG = pop_loadxdf(FILE , 'streamname', 'openbci_eeg', 'streamtype', 'EEG', 'exclude_markerstreams', {});
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 0,'setname','raw','gui','off'); 
EEG = eeg_checkset( EEG );
[EEG ALLEEG CURRENTSET] = eeg_retrieve(ALLEEG,1);
EEG=pop_chanedit(EEG, 'lookup','/home/ibagon/eeglab13_6_5b/plugins/dipfit2.3/standard_BESA/standard-10-5-cap385.elp');
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);

% Reject Channels
[EEG, indelec, measure, com] = pop_rejchan(EEG, 'elec',[1:8] ,'threshold',5,'norm','on','measure','kurt');
EEG = eeg_checkset( EEG );
display(channel_idx)
channel_idx = channel_idx(1:length(channel_idx)-length(indelec))
display(channel_idx)
% 
% % Filter set (Bandpass 1-15)
EEG = pop_eegfiltnew(EEG, [], 2, 826, true, [], 0);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 1,'setname','filtered','gui','off'); 
EEG = pop_eegfiltnew(EEG, [], 15, 220, 0, [], 0);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 2,'overwrite','on','gui','off'); 
EEG = eeg_checkset( EEG );
% % % 
% % % % 
% % % % 
% Extract Epochs
EEG = pop_epoch( EEG, {  'Correct'  'Incorrect'  }, [-0.2 0.8], 'newname', 'raw epochs', 'epochinfo', 'yes');
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 2,'gui','off'); 
EEG = eeg_checkset( EEG );

% Subsample Epochs
num_correct=0;
num_incorrect=0;
for i = 1:length(EEG.event)
	if isequal(EEG.event(i).type,'Correct')
		num_correct = 1 + num_correct;
	else if isequal(EEG.event(i).type,'Incorrect')
		num_incorrect = 1 + num_incorrect;
	end
end
end
num_total = num_correct + num_incorrect;

subsample_size = 4 * (num_incorrect);
removed=[];
while length(removed) < subsample_size
	idx = randi(num_total);
	if isequal(EEG.event(idx).type,'Correct')
		removed = [removed idx];
	end
end

% Save processed set for calibration
EEG = pop_rejepoch( EEG,removed,0);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 2,'setname','subsampled','gui','off'); 
EEG = pop_saveset( EEG, 'filename',[filename '-subsampled.set'],'filepath',['/home/ibagon/Documents/Research/RL_BCI/data/' filename '/']);
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
display(indelec)

%Time Series
[EEG ALLEEG CURRENTSET] = eeg_retrieve(ALLEEG,4);
EEG = eeg_checkset( EEG );
pop_eegplot( EEG, 1, 1, 1);

% Plot ERP Image
[EEG ALLEEG CURRENTSET] = eeg_retrieve(ALLEEG,4);
EEG = eeg_checkset( EEG );
figure; pop_erpimage(EEG,1, channel_idx,[[]],'Incorrect ERP Image',10,1,{ 'Incorrect'},[],'type' ,'yerplabel','\muV','erp','on','cbar','on','topo', { [] EEG.chanlocs EEG.chaninfo } )
print(['/home/ibagon/Documents/Research/RL_BCI/data/' filename '/Incorrect-ERPImage'],'-dpng')
figure; pop_erpimage(EEG,1, channel_idx,[[]],'Correct ERP Image',10,1,{ 'Correct'},[],'type' ,'yerplabel','\muV','erp','on','cbar','on','topo', { [] EEG.chanlocs EEG.chaninfo } )
print(['/home/ibagon/Documents/Research/RL_BCI/data/' filename '/Correct-ERPImage'],'-dpng')
EEG = eeg_checkset( EEG );
EEG = pop_selectevent( EEG, 'type',{'Incorrect'},'deleteevents','off','deleteepochs','on','invertepochs','off');
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 4,'setname','Incorrect','gui','off'); 
EEG = eeg_checkset( EEG );
figure; pop_plottopo(EEG, [1:7] , 'Incorrect', 0, 'ydir',1);
print(['/home/ibagon/Documents/Research/RL_BCI/data/' filename '/Incorrect-Topo'],'-dpng')
EEG = eeg_checkset( EEG );
figure; pop_timtopo(EEG, [-200  796], [300], 'ERP data and scalp maps of Incorrect');
print(['/home/ibagon/Documents/Research/RL_BCI/data/' filename '/Incorrect-TimTopo'],'-dpng')
% 
% 
% 
% 
% 
% 
% 
